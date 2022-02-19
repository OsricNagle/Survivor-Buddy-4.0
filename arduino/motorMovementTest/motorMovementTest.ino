#include "C:\Users\osric\Documents\GitHub\Survivor-Buddy-4.0\arduino\motorMovement\VarSpeedServo.cpp"

int servo = 5;
int feedback = A0;
int base_1 = 3;
int base_2 = 4;

VarSpeedServo test;
VarSpeedServo base1;
VarSpeedServo base2;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.setTimeout(100);

  pinMode(servo, OUTPUT);
  pinMode(feedback, INPUT);
  pinMode(base_1, OUTPUT);
  pinMode(base_2, OUTPUT);

  test.attach(servo);
  base1.attach(base_1);
  base2.attach(base_2);
}

void loop() {
  // put your main code here, to run repeatedly:
  test.write(0);
  bool impaired = test.wait(feedback);
  Serial.println("Impaired = " + String(impaired));
  delay(500);
  test.write(90);
  impaired = test.wait(feedback);
  Serial.println("Impaired = " + String(impaired));
  delay(500);

//  test.write(180);
//  Serial.println("Position: " + String(analogRead(feedback)));
//  delay(1000);
}
