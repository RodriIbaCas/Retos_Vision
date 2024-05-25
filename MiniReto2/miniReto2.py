import cv2 as cv
import numpy as np

def manualCanny(image, tresh_low, tresh_high):
    # Aplicar filtro Sobel en dirección x e y en un kernel de 3x3
    sobelx = cv.Sobel(image, cv.CV_64F, 1, 0, ksize=3)
    sobely = cv.Sobel(image, cv.CV_64F, 0, 1, ksize=3)
    
    gradient_magnitude = np.sqrt(sobelx**2 + sobely**2) # Cambios bruscos de intensidad en la imagen de los diferenciales del sobel
    gradient_magnitude *= 255.0 / gradient_magnitude.max() # Escalar los valores para que estén en el rango de 0 a 255 (mejor distinción de bordes)
    
    edges = np.zeros_like(gradient_magnitude)  # Matriz de ceros con las mismas dimensiones que gradient_magnitude 
    edges[(gradient_magnitude >= tresh_low) & (gradient_magnitude <= tresh_high)] = 255 # Asignar 255 a los bordes detectados en el rango de los umbrales
    return edges

camera = cv.VideoCapture('Recursos/Videos/dog.mp4')

while True:
    _, frame = camera.read()
    cv.imshow('Camara', frame)

    frame1 = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    edges1 = manualCanny(frame1, 30, 100) 
    cv.imshow('Canny Filter (Manual)', edges1)

    cannyEdges = cv.Canny(frame, 80, 90)
    #cv.imshow('Canny', cannyEdges)


    if cv.waitKey(5) == ord('x'):
        break

camera.release()
cv.destroyAllWindows()