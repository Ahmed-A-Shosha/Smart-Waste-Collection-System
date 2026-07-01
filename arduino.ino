#include <Servo.h>

char cmd;

// Motor Pins
int IN1 = 8, IN2 = 9, IN3 = 10, IN4 = 11;

// Front Ultrasonic
int trigFront = 6, echoFront = 7;

// Bin Ultrasonic
int trigBin = 4, echoBin = 3;

// Lid Ultrasonic
int trigLid = 12, echoLid = 13;

Servo myServo;

bool allowMovement = false;
bool sent70 = false, sent90 = false;

int lastLevel = -1, lastServoPos = -1;

int emptyDist = 15, fullDist = 5;

void setup() {
  Serial.begin(9600);
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  pinMode(trigFront, OUTPUT); pinMode(echoFront, INPUT);
  pinMode(trigBin, OUTPUT); pinMode(echoBin, INPUT);
  pinMode(trigLid, OUTPUT); pinMode(echoLid, INPUT);
  myServo.attach(2);
  myServo.write(0);
  lastServoPos = 0;
}

long getDistance(int trig, int echo) {
  digitalWrite(trig, LOW); delayMicroseconds(2);
  digitalWrite(trig, HIGH); delayMicroseconds(10);
  digitalWrite(trig, LOW);
  long duration = pulseIn(echo, HIGH, 30000);
  if (duration == 0) return -1;
  return duration * 0.034 / 2;
}

void forward() { digitalWrite(IN1,HIGH);digitalWrite(IN2,LOW);digitalWrite(IN3,HIGH);digitalWrite(IN4,LOW); }
void left()    { digitalWrite(IN1,LOW);digitalWrite(IN2,HIGH);digitalWrite(IN3,HIGH);digitalWrite(IN4,LOW); }
void right()   { digitalWrite(IN1,HIGH);digitalWrite(IN2,LOW);digitalWrite(IN3,LOW);digitalWrite(IN4,HIGH); }
void stopCar() { digitalWrite(IN1,LOW);digitalWrite(IN2,LOW);digitalWrite(IN3,LOW);digitalWrite(IN4,LOW); }

void loop() {
  // Smart Lid
  long lidDistance = getDistance(trigLid, echoLid);
  if (lidDistance > 0) {
    if (lidDistance < 50 && lastServoPos != 70) { myServo.write(70); lastServoPos = 70; }
    else if (lidDistance >= 50 && lastServoPos != 0) { myServo.write(0); lastServoPos = 0; }
  }

  // Bin Level
  if (!allowMovement) {
    long binDistance = getDistance(trigBin, echoBin);
    if (binDistance > 0 && binDistance < 100) {
      int rawPercent = map(binDistance, emptyDist, fullDist, 0, 100);
      rawPercent = constrain(rawPercent, 0, 100);
      if (binDistance >= emptyDist) rawPercent = 0;
      int level = (rawPercent / 10) * 10;
      if (level != lastLevel) { Serial.print("LEVEL:"); Serial.println(level); lastLevel = level; }
      if (level >= 70 && !sent70) { Serial.println("BIN_70"); sent70 = true; }
      if (level >= 90 && !sent90) { Serial.println("BIN_MOVING"); sent90 = true; allowMovement = true; }
    }
  }

  // Front Safety
  long frontDistance = getDistance(trigFront, echoFront);
  if (frontDistance > 0 && frontDistance < 20) { stopCar(); return; }

  if (!allowMovement) { stopCar(); return; }

  // AI Commands
  if (Serial.available()) {
    cmd = Serial.read();
    if (cmd == 'F') forward();
    else if (cmd == 'L') left();
    else if (cmd == 'R') right();
    else stopCar();
  }
}
