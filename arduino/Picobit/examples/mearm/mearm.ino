#include "Arduino.h"
#include "Servo.h"
#include "Bubbleworks_PicoBit.h"

Servo base;
Servo right;
Servo left;
Servo grip;

void setup() {

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(P3, INPUT);

  // Start serial, or timeout if not connected.
  int timeout = millis() + 2000;
  Serial.begin(115200);
  while (!Serial && millis() < timeout) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
    delay(50);
  }

  base.attach(P13);
  right.attach(P15);
  left.attach(P14);
  grip.attach(P16);

}

void loop() {

  int j0 = analogRead(P0);
  int j1 = analogRead(P1);
  int j2 = analogRead(P2);
  int j3 = digitalRead(P3);

  j0 = map(j0, 0, 1023, 179, 0);
  j1 = map(j1, 0, 1023, 0, 135);
  j2 = map(j2, 0, 1023, 30, 160);

  Serial.print(j0);
  Serial.print(", ");
  Serial.print(j1);
  Serial.print(", ");
  Serial.print(j2);
  Serial.print(", ");
  Serial.println(j3);


  base.write(j0);
  right.write(j1);
  left.write(j2);
  grip.write(45 + j3 * 60);
  delay(50);
}
