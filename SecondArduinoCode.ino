// Burned into Second Arduino 06 07 2023
#include <Stepper.h>

const int stepsPerRevolution = 360;
Stepper myStepper(stepsPerRevolution, 10, 11, 12, 13);

const int pingPin1 = 2;
const int echoPin1 = 3;

const int pingPin2 = 4;
const int echoPin2 = 5;

const int pingPin3 = 6;
const int echoPin3 = 7;

const int pingPin4 = 8;
const int echoPin4 = 9;

const int w = 250; // in mm
const int h = 150; // in mm
float wobj, hobj;

const int pinA0 = A0;
const int pinA1 = A1;
int readd1 = 0;
int readd2 = 0;

//bool fingersOpened = false; // Track the state of the fingers

void setup() {
  pinMode(pinA0, INPUT);
  pinMode(pinA1, INPUT);
  
  myStepper.setSpeed(60);
  
  Serial.begin(9600);
}

void loop() {
  readd1 = analogRead(pinA0);
  readd2 = analogRead(pinA1);

  long duration1, inches1, cm1;
  long duration2, inches2, cm2;
  long duration3, inches3, cm3;
  long duration4, inches4, cm4;

  // Read distance from Sensor 1
  duration1 = getUltrasonicDistance(pingPin1, echoPin1, inches1, cm1);
  // Read distance from Sensor 2
  duration2 = getUltrasonicDistance(pingPin2, echoPin2, inches2, cm2);
  // Read distance from Sensor 3
  duration3 = getUltrasonicDistance(pingPin3, echoPin3, inches3, cm3);
  // Read distance from Sensor 4
  duration4 = getUltrasonicDistance(pingPin4, echoPin4, inches4, cm4);

  // object size calculation in millimeters
  wobj = w - (cm1 * 10) - (cm3 * 10);
  hobj = h - (cm2 * 10) - (cm4 * 10);

  Serial.print("wobj =  ");
  Serial.print(wobj);
  Serial.print("\t");
  Serial.print("hobj =  ");
  Serial.print(hobj);
  Serial.print("\t\t");

  // Print distance readings to Serial Monitor
  printSensorReading("Sensor 1", inches1, cm1);
  printSensorReading("Sensor 2", inches2, cm2);
  printSensorReading("Sensor 3", inches3, cm3);
  printSensorReading("Sensor 4", inches4, cm4);

  delay(1000);

  if (readd1 < 200 && readd2 < 200) 
  {
    GripClose();
    delay(1000);
    //fingersOpened = true; // Update the state of the fingers
    } 
  else if ((readd1 < 200 && readd2 > 200) && (wobj <= 0 || hobj <= 0)) {
    GripOpen();
    delay(1000);
    //fingersOpened = false; // Reset the state of the fingers
  }
  else
  {
    readd1=readd2=6000;
  }
}

long getUltrasonicDistance(int triggerPin, int echoPin, long& inches, long& cm) {
  pinMode(triggerPin, OUTPUT);
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);

  pinMode(echoPin, INPUT);
  long duration = pulseIn(echoPin, HIGH);
  inches = microsecondsToInches(duration);
  cm = microsecondsToCentimeters(duration);

  return duration;
}

long microsecondsToInches(long microseconds) {
  return microseconds / 74 / 2;
}

long microsecondsToCentimeters(long microseconds) {
  return microseconds / 29 / 2;
}

void printSensorReading(const char* sensorName, long inches, long cm) {
  Serial.print(sensorName);
  Serial.print(": ");
  Serial.print(inches);
  Serial.print("in, ");
  Serial.print(cm);
  Serial.print("cm");
  Serial.println();
}

void GripOpen() {
  myStepper.step(stepsPerRevolution);
}

void GripClose() {
  myStepper.step(-stepsPerRevolution);
}
