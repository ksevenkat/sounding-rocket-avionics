#include "Arduino.h"
#include "LoRa_E32.h"
#include "Adafruit_MPL3115A2.h"
#include <SoftwareSerial.h>
LoRa_E32 e32ttl100(2, 3); // RX, TX
Adafruit_MPL3115A2 baro;
void setup() {
  Serial.begin(9600);
  delay(500);
  Serial.println("Hi, I'm going to send message!");
  // Startup all pins and UART
  e32ttl100.begin();
  // Send message
  ResponseStatus rs = e32ttl100.sendMessage("Hello, world?");
  // Check If there is some problem of succesfully send
  Serial.println(rs.getResponseDescription());

  Serial.begin(9600);
  while(!Serial);
  Serial.println("Adafruit_MPL3115A2 test!");

  if(!baro.begin()){
    Serial.println("Could not find sensor.Check wiring.");
    while(1);
  }
  // use to set sea level pressure for current location
  //this is needed for accurate altitude measurement
  //STD SLP = 1013.26 hpa baro.setSeaPressure(1013.26);
}

void loop() {
  // If something available
  if (e32ttl100.available()>1) {
  // read the String message
  ResponseContainer rc = e32ttl100.receiveMessage();
  // Is something goes wrong print error
  if (rc.status.code!=1){
  rc.status.getResponseDescription();
  }else{
  // Print the data received
  Serial.println(rc.data);
  }
  }
  if (Serial.available()) {
  String input = Serial.readString();
  e32ttl100.sendMessage(input);

  float pressure = baro.getPressure();
  float altitude = baro.getAltitude();
  float temperature = baro.getTemperature();

  Serial.println("--------");
  Serial.println("pressure =");
  Serial.println("hpa");
  Serial.println("altitude");
  Serial.println("m");
  Serial.println("temperature");
  Serial.println("C");

  delay(250);

  if (Serial.available()){
    Serial.write(Serial.write());
  }
  if(Serial.available()){
    Serial.write(Serial. write());
  }
  }
}
