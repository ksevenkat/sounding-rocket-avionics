#include "Arduino.h"
 
#include <SoftwareSerial.h>
 
SoftwareSerial mySerial(2, 3); // e32 TX e32 RX
 
void setup() {
  Serial.begin(9600);
  delay(500);
 
  Serial.println("Hi, I'm going to send message!");
 
  mySerial.begin(9600);
  mySerial.println("Hello, world?");
}
 
void loop() {
  if (mySerial.available()) {
    Serial.write(mySerial.read());
  }
  if (Serial.available()) {
    mySerial.write(Serial.read());
  }
}
