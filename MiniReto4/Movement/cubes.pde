class Cubes {
  PVector cubePos;
  PVector prevCubePos;
  boolean crash;

  float w = 20, h = 20, d = 20; //Dimensiones de los cubos
  float rotation;
  int floor = -68;
  float hitBox = (w+h+d)/3;

  //Constructor de la Clase, recibe posicion inicial y rotacion
  Cubes(float xC, float yTC, float Zc, float rYC) {
    float yC = yTC + floor + h/2;
    cubePos = new PVector(xC, yC, Zc);
    rotation = rYC;
  }

  //Actualizar posicion de los cubos
  void updatePos(float xCol, float yCol, float zCol) {
    // Traduccion de Marcos de Referecnia (Robot -> Processing)
    float xP = -yCol;
    float yP = -zCol;
    float zP = -xCol;
    // Actualizar la posicion
    cubePos.x = xP;
    cubePos.y = yP;
    cubePos.z = zP;
  }

  // Revisar colision del brazo con los cubos
  boolean checkCollisions(float xCol, float yCol, float zCol) {
    // Traduccion de Marcos de Referecnia (Robot -> Processing)
    float xP = -yCol;
    float yP = -zCol;
    float zP = -xCol;
    //Calculo del end-effector del robot y un rango al centro de la caja para ver
    //Si se tocan o no
    PVector distanceV = new PVector(cubePos.x - xP, cubePos.y - yP, cubePos.z - zP);
    float mag = distanceV.mag();
    if (mag < hitBox) {
      return true;
    } else {
      return false;
    }
  }

  // Colisiones con otros cubos
  boolean checkCubesCollisions(Cubes other) {
    PVector distanceV = PVector.sub(other.cubePos, cubePos);
    float mag = distanceV.mag();
    if (mag <= hitBox) {
      cubePos = prevCubePos;
      return crash = true;
    } else {
      return crash = false;
    }
  }

  // Si el cubo no esta siendo agarradi ni en contacto con otro, este caera hasta el piso
  void fall() {
    if (!crash && !grab && cubePos.y > floor + h/2) {
      cubePos.y -= 0.1*(millisOld - gTime);
    }
  }
  
  // Ejecutar funciones y mostrar el cubo
  void display(){
  //Asegurar que la caja este sobre el piso
    if(cubePos.y < floor + h/2){
      cubePos.y = floor + h/2;
    }
    fill(120,120,60);
    pushMatrix();
    translate(cubePos.x, cubePos.y, cubePos.z);
    rotateY(rotation);
    box(w, h, d);
    popMatrix();
    prevCubePos = cubePos.copy();
  }
  
}
