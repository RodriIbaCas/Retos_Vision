void updatePosition() {
  if (movements != null) {
    for (String instruction : movements) {
      switch(instruction) {
      case "Abajo":
        if (posZ < maxZ) posZ += stepSize;
        break;
      case "Arriba":
        if (posZ > minZ) posZ -= stepSize;
        break;
      case "Izquierda":
        if (posX > minX) posX -= stepSize;
        break;
      case "Derecha":
        if (posX < maxX) posX += stepSize;
        break;
      case "Atras":
        if (posY < maxY) posY += stepSize;
        break;
      case "Adelante":
        if (posY > minY) posY -= stepSize;
        break;
      }
    }
  }
  if (states != null) {
    for (String state : states) {
      switch(state) {
        case "Abierta" : grab = false; break;
        case "Cerrada" : grab = true; break;
      }
    }
  }
}



//Movimiento con el teclado para testing


//boolean moveForward, moveBackward, moveLeft, moveRight, moveUp, moveDown;

//void keyPressed() {
//    switch(key) {
//        case 'w': moveForward = true; break;
//        case 's': moveBackward = true; break;
//        case 'a': moveLeft = true; break;
//        case 'd': moveRight = true; break;
//        case 'q': moveUp = true; break;
//        case 'e': moveDown = true; break;
//        case 'g': grab = true; break;  // Toggle grab state
//        case 'h': grab = false; break;
//    }
//}

//void keyReleased() {
//  switch(key) {
//    case 'w': moveForward = false; break;
//    case 's': moveBackward = false; break;
//    case 'a': moveLeft = false; break;
//    case 'd': moveRight = false; break;
//    case 'q': moveUp = false; break;
//    case 'e': moveDown = false; break;
//  }
//}

//void updatePosition() {
//  if (moveForward && posZ < maxZ) posZ += stepSize;
//  if (moveBackward && posZ > minZ) posZ -= stepSize;
//  if (moveLeft && posX > minX) posX -= stepSize;
//  if (moveRight && posX < maxX) posX += stepSize;
//  if (moveUp && posY < maxY) posY += stepSize;
//  if (moveDown && posY > minY) posY -= stepSize;
//}
