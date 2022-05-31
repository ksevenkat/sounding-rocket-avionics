#include <Adafruit_MPL3115A2.h>
#include <Servo.h>
Adafruit_MPL3115A2 baro;
Servo myservo;
int potpin =A0;
int val;
const int a;
const int b;
int pin = 2;
void setup() {
pinMode(3,OUTPUT);
digitalWrite (3, HIGH);
myservo.attach(2);
  Serial.begin(9600);
  while(!Serial);
  Serial.println("Adafruit_MPL3115A2 test!");

  if (!baro.begin()) {
    Serial.println("Could not find sensor. Check wiring.");
    while(1);
  }

  // use to set sea level pressure for current location
  // this is needed for accurate altitude measurement
  // STD SLP = 1013.26 hPa
  baro.setSeaPressure(1013.26);
}

void loop() {
  float pressure = baro.getPressure();
  float altitude = baro.getAltitude();
  float temperature = baro.getTemperature();
//  float altitude = altitude();
  Serial.print("Altitude(m):");
  Serial.print(altitude, 2);

  Serial.println("-----------------");
  Serial.print("pressure = "); Serial.print(pressure); Serial.println(" hPa");
  Serial.print("altitude = "); Serial.print(altitude); Serial.println(" m");
  Serial.print("temperature = "); Serial.print(temperature); Serial.println(" C");


  delay(250);

  
if ( altitude >= 307)
{
digitalWrite(3, LOW);
myservo.write(45);
delay (2000);
}

else
{
  digitalWrite (3, HIGH);
  myservo.write(0);


}



}
