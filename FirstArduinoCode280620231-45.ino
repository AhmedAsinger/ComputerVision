#include <Servo.h>
// Burned to the Arduino1 10 07 2023 4:47 pm

// Servo objects for each finger
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;

// Pins for communication with the second Arduino
const int communicationPin1 = 2;
const int communicationPin2 = 3;

// Initial positions for the fingers
const int initialPositions[] = {0, 90, 0, 90, 0, 90};

// Configurations for different shapes
const int circularShapePositions[] = {30, 60, 30, 60, 30, 60};
const int rectangleShapePositions[] = {0, 90, 30, 60, 30, 60};
const int triangleShapePositions[] = {0, 90, 0, 90, 0, 90};

// Delay duration for servo movements
const int servoDelay = 2000;

void setup() {
  pinMode(communicationPin1, OUTPUT);
  pinMode(communicationPin2, OUTPUT);
  
  Serial.begin(9600);
  
  servo1.attach(13);
  servo2.attach(12);
  servo3.attach(11);
  servo4.attach(10);
  servo5.attach(9);
  servo6.attach(8);
  
  setFingerPositions(initialPositions);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    switch (command) {
      case 'H':{
           moveFingersToHomePosition();
        break;
      }
      case 'C':{
          configureFingers(circularShapePositions);
        break;
      }
      case 'R':{
          configureFingers(rectangleShapePositions);
        break;
      }
      case 'T':{
          configureFingers(triangleShapePositions);
          break;
          }
      case 'L':{
        digitalWrite(communicationPin1, HIGH);
        digitalWrite(communicationPin2, LOW);
        break;
        }
      case 'U':// OPEN FINGERS
      {
        digitalWrite(communicationPin1, LOW);
        digitalWrite(communicationPin2, HIGH);
        break;
      }
      case 'D':// close fingers
      {
        digitalWrite(communicationPin1, LOW);
        digitalWrite(communicationPin2, LOW);
        break;
      }
    }
  }
}

void setFingerPositions(const int positions[]) {
  servo1.write(positions[0]);
  servo2.write(positions[1]);
  servo3.write(positions[2]);
  servo4.write(positions[3]);
  servo5.write(positions[4]);
  servo6.write(positions[5]);
  
  delay(servoDelay);
}

void moveFingersToHomePosition() {
  setFingerPositions(initialPositions);
}

void configureFingers(const int positions[]) {
  moveFingersToHomePosition();
  
  setFingerPositions(positions);
  
  digitalWrite(communicationPin1, HIGH);
  digitalWrite(communicationPin2, HIGH);
  Serial.write('A');
}
