PShape base, shoulder, upArm, loArm, end;
float rotX, rotY;
float posX=1, posY=50, posZ=50;

float millisOld, gTime, gSpeed = 4;


float stepSize = 0.5;
boolean grab = false, crash;



String[] movements;
String[] states;

Cubes[] cubes = {
  new Cubes(65, 0, -65, 0),
  new Cubes(65, 40, -65, 0),
  new Cubes(3, 0, -35, 0),
  new Cubes(45, 0, 20, 0),
  new Cubes(39, 0, -29, 0)
};

int[] crashCount = new int[cubes.length];
boolean[] crashed = new boolean[cubes.length];


void setTime() {
  gTime += ((float)millis()/1000 - millisOld)*(gSpeed/4);
  if (gTime >= 4)  gTime = 0;
  millisOld = (float)millis()/1000;
}



void writePos() {
  updatePosition();
  IK();
}


float[] Xsphere = new float[99];
float[] Ysphere = new float[99];
float[] Zsphere = new float[99];

void setup() {
  size(1200, 800, OPENGL);


  base = loadShape("r5.obj");
  shoulder = loadShape("r1.obj");
  upArm = loadShape("r2.obj");
  loArm = loadShape("r3.obj");
  end = loadShape("r4.obj");

  shoulder.disableStyle();
  upArm.disableStyle();
  loArm.disableStyle();
}

void draw() {
  movements = loadStrings("movement_direction.txt");
  states = loadStrings("hand_state.txt");


  writePos();
  setTime();


  background(31);
  smooth();
  lights();
  directionalLight(51, 102, 126, -1, 0, 0);
  fill(255, 255, 255);
  noStroke();

  translate(width/2, height/2);

  rotateX(rotX);
  rotateY(-rotY);
  scale(-4);

  //Suelo
  pushMatrix();
  translate(0, -68, 0);
  box(300, 2, 300);
  popMatrix();


  pushMatrix();
  fill(150, 0, 150);
  //Coloca la referencia de la base
  translate(0, -40, 0);
  shape(base);

  //Coloca la referencia de la primera articulación
  translate(0, 4, 0);
  rotateY(gamma);
  shape(shoulder);

  //Coloca la referencia de la segunda articulación
  translate(0, 25, 0);
  rotateY(PI);
  rotateX(alpha);
  shape(upArm);

  //Coloca la referencia de la tercera articulación
  translate(0, 0, 50);
  rotateY(PI);
  rotateX(beta);
  shape(loArm);

  //Coloca la referencia del último componente
  translate(0, 0, -50);
  rotateY(PI);
  shape(end);
  popMatrix();

  //Insertar los cubos
  for (int i = 0; i<cubes.length; i++) {
    cubes[i].display();
    // Revisar si el brazo esta tocando la cubos
    if (cubes[i].checkCollisions(posX, posY, posZ) && grab) {
      cubes[i].updatePos(posX, posY, posZ);
    }
    //Revisar colisiones entre cubos
    crashCount[i] = 0;
    for (int j = 0; j<cubes.length; j++) {
      if (j != 1) {
        crash = cubes[i].checkCubesCollisions(cubes[j]);
        if (crash) {
          crashed[i] = true;
          crashCount[i] += 1;
        }
      }
    }
    if (crashCount[i] == 0) {
      crashed[i] = false;
    }
    if (!crashed[i]) {
      cubes[i].fall();
    }
  }
}

void mouseDragged() {
  rotY -= (mouseX - pmouseX) * 0.01;
  rotX -= (mouseY - pmouseY) * 0.01;
}
