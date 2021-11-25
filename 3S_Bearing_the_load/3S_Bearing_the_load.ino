int Vo;
int microphone;
float R1 = 10000;
float logR2, R2, temp, temp_C;
float c1 = 1.129252142e-03, c2 = 2.341083183e-04, c3 = 0.8773267909e-07;
//Steinhart–Hart equation Calculator https://www.thinksrs.com/downloads/programs/therm%20calc/ntccalibrator/ntccalculator.html
void setup() {
  // open a serial connection
  Serial.begin(115200);
  
}

void loop() {
  //Accelerometer 
//   analogReadResolution(10);
//   Serial.print("ADC 10-bit (default) : ");
//   Serial.println(analogRead(A0));
  //Temperature sensor
  Vo = analogRead(A1);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  temp = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  temp_C = temp - 273.15;
  //Microphone
  microphone  = analogRead(A2);
  //Test Output
  // Serial.print(" A2: ");
  // Serial.print("Temperature: "); 
  // Serial.print(temp_C);
  // Serial.print(" C");
  // Serial.print(" R2: ");
  // Serial.println(R2);
  // Serial.println(microphone);
  //CSV Output
  Serial.println(String(temp_C) + ","+ String(microphone)); //
  delay(100);
}
