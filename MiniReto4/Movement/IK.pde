float F = 50;
float T = 70;

float alpha, beta, gamma;

float minX = -68, maxX = 68;
float minY = -68, maxY = 68;
float minZ = -68, maxZ = 62;

void IK() {
  float X = posX;
  float Y = posY;
  float Z = posZ;
  

  float L = sqrt(Y*Y+X*X);
  float dia = sqrt(Z*Z+L*L);

  alpha = PI/2-(atan2(L, Z)+acos((T*T-F*F-dia*dia)/(-2*F*dia)));
  beta = -PI+acos((dia*dia-T*T-F*F)/(-2*F*T));
  gamma = atan2(Y, X);
}
