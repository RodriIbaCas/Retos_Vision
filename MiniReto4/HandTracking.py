import cv2 as cv
import mediapipe as mp
import time


# Clase para detectar el movimiento de la mano, (min_detection y min_tracking por default)
# Variar tresholds por si se quiere cambiar la sensibilidad del movimiento
class HandMovementDetector: 
    def __init__(self, camera_index=1, min_detection_confidence=0.75, min_tracking_confidence=0.75, 
                 movement_threshold=20, area_change_threshold=1500, movement_file="Movement/movement_direction.txt", 
                 state_file="Movement/hand_state.txt", still_file="Movement/still_hand.txt", update_interval=2.0, still_interval=2.0): 
        

        
        self.video = cv.VideoCapture(camera_index) #Abrir la camara 
        if not self.video.isOpened():
            raise IOError("Error: Camera could not be opened.")
        
        # Configuracion de la deteccion de manos de mediapipe
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(min_detection_confidence=min_detection_confidence, min_tracking_confidence=min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

        # Variables para detectar el movimiento de la mano en el plano XY
        self.previous_x_center = None
        self.previous_y_center = None
        self.previous_area = 0 # Variable para detectar el movimiento de la mano en el plano Z

        self.movement_threshold = movement_threshold # Treshold para detectar el movimiento de la mano en el plano XY
        self.area_change_threshold = area_change_threshold # Treshold para detectar el movimiento de la mano en el plano Z

        self.movement_file = movement_file # Archivo para guardar la direccion del movimiento de la mano
        self.state_file = state_file # Archivo para guardar el estado de la mano

        self.update_interval = update_interval
        self.still_interval = still_interval
        self.last_update_time = 0
        self.last_movement_time = time.time() # Tiempo del ultimo movimiento detectado
        self.still_message_sent = False

    def write_movement_to_file(self, direction): # Escribe la direccion del movimiento de la mano en un archivo de texto
        with open(self.movement_file, "w") as file:
            file.write(direction)

    def write_state_to_file(self, state): # Escribe el estado de la mano en un archivo de texto
        """Writes the detected hand state to a text file."""
        with open(self.state_file, "w") as file:
            file.write(state)
    
    def detect_xy_movement(self, current_x_center, current_y_center): # Detectar movimiento plano XY
        direction = "" 
        if self.previous_x_center is not None and self.previous_y_center is not None:
            x_diff = current_x_center - self.previous_x_center # Diferencia en x 
            y_diff = current_y_center - self.previous_y_center # Diferencia en y 

            if abs(x_diff) > self.movement_threshold:
                direction = "Derecha" if x_diff > 0 else "Izquierda" # Movimiento en x dependiendoo de la diferencia con el frame anterior

            if abs(y_diff) > self.movement_threshold:
                direction = "Abajo" if y_diff > 0 else "Arriba" # Movimiento en y dependiendo de la diferencia con el frame anterior

            if direction:
                print(direction) # Imprimir la direccion del movimiento
                self.write_movement_to_file(direction)
                self.last_movement_time = time.time()
                self.still_message_sent = False

    def detect_z_movement(self, current_area): # Detectar movimiento en el plano Z
        area_direction = ""
        if self.previous_area != 0 and abs(current_area - self.previous_area) > self.area_change_threshold: # Diferencia en el area de la mano
            area_direction = "Adelante" if current_area > self.previous_area else "Atras"
            
            if area_direction:
                print(area_direction)
                self.write_movement_to_file(area_direction) # Escribir la direccion del movimiento en un archivo de texto
                self.last_movement_time = time.time()
                self.still_message_sent = False

    def calculate_bounding_box(self, landmarks, img_shape): # Calcular el bounding box de la mano
        x_min, y_min = float('inf'), float('inf') # Inicializar los valores minimos y maximos
        x_max, y_max = 0, 0 # Inicializar los valores minimos y maximos

        for id in [0, 1, 5, 9, 13]: # Iterar sobre los landmarks de la mano (WRISTH, THUMB CMC, INDEX FINGER, MIDDLE FINGER, RING FINGER)
            lm = landmarks[id] # Obtener el landmark
            x, y = int(lm.x * img_shape[1]), int(lm.y * img_shape[0]) # Obtener las coordenadas del landmark en pixeles
            x_min, x_max = min(x, x_min), max(x, x_max) 
            y_min, y_max = min(y, y_min), max(y, y_max)
        
        current_x_center = (x_min + x_max) // 2 # Calcular el centro de la mano
        current_y_center = (y_min + y_max) // 2 # Calcular el centro de la mano
        current_area = (x_max - x_min) * (y_max - y_min) # Calcular el area de la mano

        return current_x_center, current_y_center, current_area, (x_min, y_min, x_max, y_max)

    def is_hand_open(self, landmarks): # Detectar si la mano esta abierta o cerrada
        # Landmarks de los dedos de la mano (puntas y nudillos)
        tip_ids = [4, 8, 12, 16, 20]
        knuckle_ids = [2, 6, 10, 14, 18]

        open_fingers = 0
        for tip_id, knuckle_id in zip(tip_ids, knuckle_ids):
            if landmarks[tip_id].y < landmarks[knuckle_id].y: # Si la punta del dedo esta arriba del nudillo
                open_fingers += 1 # Contar el dedo como abierto
        
        return open_fingers >= 4 # Si 4 dedos estan abiertos, la mano esta abierta

    def detect_movement(self): # Detectar el movimiento de la mano
        try:
            while True:
                success, img = self.video.read()
                if not success:
                    print("Failed to capture image")
                    break

                imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB) # Convertir la imagen a RGB
                results = self.hands.process(imgRGB) # Procesar la imagen para detectar las manos

                if results.multi_hand_landmarks: # Si se detectan manos
                    for handLms in results.multi_hand_landmarks: # Iterar sobre las manos detectadas 
                        self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) # Dibujar los landmarks de la mano

                        current_x_center, current_y_center, current_area, bbox = self.calculate_bounding_box(handLms.landmark, img.shape) # Calcular el bounding box de la mano
                        
                        cv.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2) # Dibujar el bounding box de la mano
                        
                        # Detectar el movimiento de la mano en los planos XY y Z
                        self.detect_xy_movement(current_x_center, current_y_center) 
                        self.detect_z_movement(current_area) 

                        current_time = time.time() # Obtener el tiempo actual
                        if current_time - self.last_update_time >= self.update_interval: # Si ha pasado el intervalo de actualizacion
                            if self.is_hand_open(handLms.landmark): # Detectar si la mano esta abierta o cerrada, mostrar en pantalla, y escribir en un archivo de texto
                                cv.putText(img, "Mano Abierta", (10, 70), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                self.write_state_to_file("Abierta")
                                print("Mano Abierta")
                            else:
                                cv.putText(img, "Mano Cerrada", (10, 70), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) 
                                self.write_state_to_file("Cerrada")
                                print("Mano Cerrada")

                            self.last_update_time = current_time
                        
                        self.previous_x_center = current_x_center
                        self.previous_y_center = current_y_center
                        self.previous_area = current_area
                

                cv.imshow('Video', img)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.video.release()
            cv.destroyAllWindows()

if __name__ == "__main__":
    detector = HandMovementDetector()
    detector.detect_movement()
