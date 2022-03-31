#include "C:\Users\osric\Documents\GitHub\Survivor-Buddy-4.0\arduino\motorMovement\VarSpeedServo.h"

//Control and Feedback Pins
//regular 180 servos
int leftBasePin = 3; 
int rightBasePin = 2; 
int leftBaseFeedback = A1; 
int rightBaseFeedback = A0; 

//360 servo
int turnTablePin = 4;
int turnTableFeedback  = A2;

//180 mini servo
int phoneMountPin = 5;
int phoneMountFeedback = A3;

//additional servo controlling phone tilt
int phoneTiltPin = 6;
int phoneTiltFeedback = A4;

int ledPin = 2;

// Position constants
const int RIGHT_BASE_DOWN = 70; // was 55
const int RIGHT_BASE_UP = 150; // was 138
const int LEFT_BASE_DOWN = 150;
const int LEFT_BASE_UP = 65;
const int PHONEMOUNT_LANDSCAPE = 25; // was 7
const int PHONEMOUNT_PORTRAIT = 110; // was 115
const int PHONEMOUNT_TILT = 60;

// Feedback constants
const int RIGHT_BASE_FB_DOWN = 186;
const int RIGHT_BASE_FB_UP = 369;
const int LEFT_BASE_FB_DOWN = 415;
const int LEFT_BASE_FB_UP = 235;
const int PHONEMOUNT_FB_PORTRAIT = 0;
const int PHONEMOUNT_FB_LANDSCAPE = 0;
const int TABLETOP_FRONT = 135; // was 120
const int TABLETOP_LEFT = 205;
const int TABLETOP_RIGHT = 25;

//Create VarSpeedServo objects 
VarSpeedServo leftBaseServo;
VarSpeedServo rightBaseServo;
VarSpeedServo tabletopServo;
VarSpeedServo phoneMountServo; 
VarSpeedServo phoneTiltServo;

enum Command {PITCH, YAW, ROLL, CLOSE, OPEN, PORTRAIT, 
              LANDSCAPE, NOD, SHAKE, TILT, SHUTDOWN};

/*******************************************************************/
/*Phone Mount Functions*/
void portrait(){ //phoneMountServo moves phone to portrait position
    phoneMountServo.write(PHONEMOUNT_PORTRAIT, 40, true);
}

void landscape(){ //phoneMountServo moves phone to landscape position
    phoneMountServo.write(PHONEMOUNT_LANDSCAPE, 40, true);
}

void tilt() {
  int currAngle = phoneMountServo.read();
  phoneMountServo.write(PHONEMOUNT_TILT, 60, true);
  delay(500);
  phoneMountServo.write(currAngle, 60, true);
}

/*
 * Get current position of Phone Mount Servo
*/
int getPositionPM(){
  int potVal = analogRead(phoneMountFeedback);
  return map(potVal, PHONEMOUNT_FB_PORTRAIT, PHONEMOUNT_FB_LANDSCAPE, 0, 90);
}
/*******************************************************************/
/*Base Motor Functions*/
/*
 * Get current position of Base Servos
*/
int getPositionBM(){
//  int potValLeft = analogRead(leftBaseFeedback);
//  int leftAngle = map(potValLeft, LEFT_BASE_FB_DOWN, LEFT_BASE_FB_UP, 0, 90);
  int potValRight = analogRead(rightBaseFeedback);
  int rightAngle = map(potValRight, RIGHT_BASE_FB_DOWN, RIGHT_BASE_FB_UP, 0, 90);
  return rightAngle;
}

// 360 parallax constants
const unsigned long unitsFC = 360; // 360 degrees in a circle
const unsigned long dcMin = 29;
const unsigned long dcMax = 971;
const unsigned long dutyScale = 1000;
// not constants, but don't want to have to declare them a lot
unsigned long tCycle, tHigh, tLow, dc;
unsigned long theta;

int getPositionTabletop(){
  int tCycle = 0;
  int tHigh, tLow, theta, dc;
  while (1) {
    tHigh = pulseIn(turnTableFeedback, HIGH);
    tLow = pulseIn(turnTableFeedback, LOW);
    tCycle = tHigh + tLow;
    if ((tCycle > 1000) && (tCycle < 1200)) {
      break;
    }
  }
  dc = (dutyScale * tHigh) / tCycle;
  theta = ((dc - dcMin) * unitsFC) / (dcMax - dcMin + 1);
  if (theta < 0) {
    theta = 0;
  }
  else if (theta > (unitsFC - 1)) {
    theta = unitsFC - 1;
  }
  return theta;
}

void up(){
  leftBaseServo.write(150, 40);
  rightBaseServo.write(30, 40);
  leftBaseServo.wait();
  rightBaseServo.wait();
}
void down(){
  leftBaseServo.write(70, 40);
  rightBaseServo.write(110, 40);
  leftBaseServo.wait();
  rightBaseServo.wait();
}
void nod(){
  //up down, arm nods twice
  int currAngleLeft = leftBaseServo.read();
  int currAngleRight = rightBaseServo.read();
  leftBaseServo.write(150, 60);
  rightBaseServo.write(30, 60);
  leftBaseServo.wait();
  rightBaseServo.wait();
  delay(100);
  leftBaseServo.write(70, 60);
  rightBaseServo.write(110, 60);
  leftBaseServo.wait();
  rightBaseServo.wait();
  delay(100);
//  leftBaseServo.write(150, 60);
//  rightBaseServo.write(30, 60);
//  leftBaseServo.wait();
//  rightBaseServo.wait();
//  delay(100);
//  leftBaseServo.write(70, 60);
//  rightBaseServo.write(110, 60);
//  leftBaseServo.wait();
//  rightBaseServo.wait();
//  delay(100);
//  leftBaseServo.write(150, 60);
//  rightBaseServo.write(30, 60);
//  leftBaseServo.wait();
//  rightBaseServo.wait();
  // leftBaseServo.write(currAngleLeft, 60, true);
  // rightBaseServo.write(currAngleRight, 60, true);
}
/*******************************************************************/
void behaviorTracking() {
  String in = "";
  writeAllServos(90, 90, 90, 90);
  int basePos, torsoPos, headRotPos, headTiltPos = 0;
  while (in.indexOf('$') == -1){
    if (Serial.available())
      in = Serial.readStringUntil('\n');
    else
      in = "";
    // Serial.println("%" + in + "%");
    // 123124125126
    if (in.equals("") == false){
      if (in.length() == 12){
        Serial.print("%" + in + "%");
        basePos = in.substring(0,3).toInt();
        torsoPos = in.substring(3,6).toInt();
        headRotPos = in.substring(6,9).toInt();
        headTiltPos = in.substring(9,12).toInt();
        // printAllServoPos(basePos, torsoPos, headRotPos, headTiltPos);
        writeAllServos(basePos, torsoPos, headRotPos, headTiltPos);
      }
      else{
        // Serial.println("printing");
        // Serial.println(in);
      }
    }
    
  } 
  // Remove extra byte sent over via Serial Arm Communicator
  // char throwaway = Serial.read();
  // Serial.print("SerBufSize = " + String(Serial.available()));
}

void writeAllServos(int basePos, int torsoPos, int headRotPos, int headTiltPos){
  // Serial.print("Moving servos");
  printAllServoPos(basePos, torsoPos, headRotPos, headTiltPos);
  leftBaseServo.write(basePos);
  leftBaseServo.wait();
  rightBaseServo.write(180-basePos);
  rightBaseServo.wait();
  tabletopServo.write(torsoPos);
  tabletopServo.wait();
  phoneMountServo.write(headRotPos);
  phoneMountServo.wait();
  phoneTiltServo.write(headTiltPos);
  phoneTiltServo.wait();
}

void printAllServoPos(int basePos, int torsoPos, int headRotPos, int headTiltPos){
  Serial.print("Base: ");
  Serial.print(basePos);
  Serial.print(", Torso: ");
  Serial.print(torsoPos);
  Serial.print(", Rot: ");
  Serial.print(headRotPos);
  Serial.print(", Tilt: ");
  Serial.println(headTiltPos);
}

/*Turn Table Motor Functions*/
void shake(){
  setYaw((TABLETOP_LEFT + TABLETOP_FRONT)/2);
  delay(100);
  setYaw((TABLETOP_RIGHT + TABLETOP_FRONT)/2);
  delay(100);
  setYaw(TABLETOP_FRONT);
}

void _shutdown() {
  setYaw(TABLETOP_FRONT);
  portrait();
  delay(100);
  down();
  delay(100);
  // blink LED then off
  for (int i = 0; i < 3; i++) {
    digitalWrite(ledPin, LOW);
    delay(500);
    digitalWrite(ledPin, HIGH);
    delay(500);
  }
  sendPosition();
  //stop all motor movement. will need to unplug and plug back in to move again
  //while(true) {}
}

/*Emergency Shut Down*/
void emergencyShutdown(){
  //stop all motor movement. will need to unplug and plug back in to move again
  while(true) {}
}



void setPitch(char val) {
  int leftVal = map(val, 0, 90, LEFT_BASE_DOWN, LEFT_BASE_UP);
  int rightVal = map(val, 0, 90, RIGHT_BASE_DOWN, RIGHT_BASE_UP);
  leftBaseServo.write(leftVal, 40);
  rightBaseServo.write(rightVal, 40);
}

void setYaw(int val) {
//  int offset = 0;
  int currPos = getPositionTabletop();
//  int diff = currPos - val; /* ATTEMPT AT PID CONTROLLER FAILED */
//  while (abs(diff) > 1) {
//    Serial.println("LOOPING");
//    offset = 0;
//    if (diff > 200) {
//      diff = 200;
//    }
//    else if (diff < -200) {
//      diff = -200;
//    }
//    if (diff > 1) {
//      offset = -30;
//    }
//    else if (diff < -1) {
//      offset = 30;
//    }
//    tabletopServo.writeMicroseconds(1500 + diff + offset);
//    currPos = getPositionTabletop();
//    diff = currPos - val;
//  }
  if (val > currPos) {
    tabletopServo.writeMicroseconds(1430);
    while (val > currPos + 10) {
      currPos = getPositionTabletop();
    }
    tabletopServo.writeMicroseconds(1440);
    while (val > currPos) {
      currPos = getPositionTabletop();
    }
  }
  else if (val < currPos) {
    tabletopServo.writeMicroseconds(1555);
    while (val < currPos - 10) {
      currPos = getPositionTabletop();
    }
    tabletopServo.writeMicroseconds(1540);
    while (val < currPos) {
      currPos = getPositionTabletop();
    }
  }
  tabletopServo.writeMicroseconds(1500);
}

void setRoll(char val) {
  int pos = map(val, 0, 90, PHONEMOUNT_PORTRAIT, PHONEMOUNT_LANDSCAPE);
  phoneMountServo.write(pos, 40, true);
}

void sendPosition() {
  char pos[3]; // [pitch, yaw, roll]
  pos[0] = map(rightBaseServo.read(), RIGHT_BASE_DOWN, RIGHT_BASE_UP, 0, 90);
  pos[1] = map(getPositionTabletop(), TABLETOP_LEFT, TABLETOP_RIGHT, 0, 180);
  pos[2] = map(phoneMountServo.read(), PHONEMOUNT_PORTRAIT, PHONEMOUNT_LANDSCAPE, 0, 90);
  Serial.write(pos, 3);
}

void test() {
  shake();
  delay(1000);
}

/*******************************************************************/
void setup() {
  Serial.begin(115200);
  // Serial.setTimeout(5000);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  // feedback pins
  pinMode(leftBaseFeedback, INPUT);
  pinMode(rightBaseFeedback, INPUT);
  pinMode(turnTableFeedback, INPUT);
  pinMode(phoneMountFeedback, INPUT);
  pinMode(phoneTiltFeedback, INPUT);

  // Serial.println("Before attaching pins");
  
  // attaches the servo on pin to the servo object
  tabletopServo.attach(turnTablePin);
  tabletopServo.attachFeedback(turnTableFeedback);
  // setYaw(TABLETOP_FRONT);
  leftBaseServo.attach(leftBasePin);  
  leftBaseServo.attachFeedback(leftBaseFeedback);
  // leftBaseServo.write(LEFT_BASE_DOWN, 60, true);
  rightBaseServo.attach(rightBasePin);
  // rightBaseServo.write(RIGHT_BASE_DOWN, 60, true);
  // rightBaseServo.write(RIGHT_BASE_UP, 60, true);
  phoneMountServo.attach(phoneMountPin);
  phoneMountServo.attachFeedback(phoneMountFeedback);
  phoneMountServo.write(PHONEMOUNT_PORTRAIT);
  phoneTiltServo.attach(phoneTiltPin);
  phoneTiltServo.attachFeedback(phoneTiltFeedback);

  // Serial.println("After attaching pins, before calibration");

  // run calibration functions for updated wait() to work correctly
//  leftBaseServo.calibratePair(&rightBaseServo);
//  tabletopServo.calibrate();
//  phoneMountServo.calibrate();
//  phoneTiltServo.calibrate();

  // Serial.print("Calibration complete");
}

//Serial Data
unsigned char serialData[128];
char data, throwaway;
unsigned long numLoops = 0;
int lastYaw = TABLETOP_FRONT;

void loop() {
  // try to keep tabletopServo from jerking
//  setYaw(lastYaw);
//  tabletopServo.writeMicroseconds(1510);
//  test();
  
  numLoops++;
  // Serial.print(data);
  if (Serial.available() > 0) {//serial is reading stuff 
    // Serial.readBytes(serialData, 2); 
    data = Serial.read();
    throwaway = Serial.read();
    // Serial.print("BufferSize = " + String(Serial.available()));
    // Serial.write(data);
    if (data == 0x00) { // set pitch
      if (0 <= serialData[1] && serialData[1] <= 90) {
        setPitch(serialData[1]);
      }
    }
    else if (data == 0x01) { // set yaw
      if (0 <= serialData[1] && serialData[1] <= 180) {
        lastYaw = map(serialData[1], 0, 180, TABLETOP_LEFT, TABLETOP_RIGHT);
        setYaw(lastYaw);
      }
    }
    else if (data == 0x02) { // set roll
      if (0 <= serialData[1] && serialData[1] <= 90) {
        setRoll(serialData[1]);
      }
    }
    else if(data == 0x03){ // close 
      down();
    }
    else if (data == 0x04){ // open
      // Serial.print("open button");
      up(); 
    }
    else if(data == 0x05){ // portrait
      portrait();
    }
    else if (data == 0x06){ // landscape
      landscape();
    } 
    else if(data == 0x07){ // nod
      nod();
    }
    else if (data == 0x08){ // shake
      lastYaw = TABLETOP_FRONT;
      shake();
    }
    else if(data == 0x09){ // tilt
      tilt();
    }
    else if (data == 0x10) { // shutdown
      _shutdown();
    } else if (data == 0x11) { // behavior tracking
      // Serial.write("Serial info passed correctly");
      writeAllServos(90, 90, 90, 90);
      behaviorTracking();
    }
  }
//  if (numLoops % 100 == 0) {
//    setYaw(lastYaw);
//    sendPosition();
//    numLoops = 0;
//  }
  
  // delay(50);
} //end loop
