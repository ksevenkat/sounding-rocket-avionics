#include <TinyGPS.h>
#include "Arduino.h"
#include<SoftwareSerial.h>
/* This sample code demonstrates the normal use of a TinyGPS object. */
TinyGPS gps;

/* On Teensy, the UART (real serial port) is always best to use. */
/* Unlike Arduino, there's no need to use NewSoftSerial because */
/* the "Serial" object uses the USB port, leaving the UART free. */
SoftwareSerial Uart(0,1);
SoftwareSerial mySerial(0, 1);
void gpsdump(TinyGPS &gps);
void printFloat(double f, int digits = 2);

void setup()
{
  Serial.begin(9600);
  Uart.begin(9600);
  
  delay(1000);
  Serial.print("Testing TinyGPS library v. "); Serial.println(TinyGPS::library_version());
  Serial.println("by Mikal Hart");
  Serial.println();
  Serial.print("Sizeof(gpsobject) = "); Serial.println(sizeof(TinyGPS));
  Serial.println();
  mySerial.begin(9600);
  mySerial.println("Hello, world?");
}

void loop()
{
  bool newdata = false;
  unsigned long start = millis();

  // Every 5 seconds we print an update
  while (millis() - start < 5000) {
    if (Uart.available()) {
      char c = Uart.read();
        //Serial.print(c);  // uncomment to see raw GPS data
      if (gps.encode(c)) {
        newdata = true;
//         break;  // uncomment to print new data immediately!
      }
    }
  }
  
  if (newdata) {
    Serial.println("Acquired Data");
    Serial.println("-------------");
    gpsdump(gps);
    Serial.println("-------------");
    Serial.println();
  }
}

void gpsdump(TinyGPS &gps)
{
  long lat, lon;
  float flat, flon;
  unsigned long age, date, time, chars;
  int year;
  byte month, day, hour, minute, second, hundredths;
  unsigned short sentences, failed;

  gps.get_position(&lat, &lon, &age);
  mySerial.write("Lat/Long(10^-5 deg): "); mySerial.print(lat); mySerial.print(", "); mySerial.print(lon); 
  mySerial.print("\nFix age: "); mySerial.print(age); mySerial.println("ms.");
  
  // On Arduino, GPS characters may be lost during lengthy Serial.print()
  // On Teensy, Serial prints to USB, which has large output buffering and
  //   runs very fast, so it's not necessary to worry about missing 4800
  //   baud GPS characters.

  gps.f_get_position(&flat, &flon, &age);
  /*mySerial.print("Lat/Long(float): "); printFloat(flat, 5); mySerial.print(", "); printFloat(flon, 5);*/
  //mySerial.print(" Fix age: "); mySerial.print(age); mySerial.println("ms.");

  gps.get_datetime(&date, &time, &age);
  mySerial.print("Date(ddmmyy): "); mySerial.print(date); mySerial.print(" Time(hhmmsscc): ");
  mySerial.print(time);
  //mySerial.print(" Fix age: "); mySerial.print(age); mySerial.println("ms.");
 mySerial.print("\n\n--------------------------\n\n");
  /*gps.crack_datetime(&year, &month, &day, &hour, &minute, &second, &hundredths, &age);
  mySerial.print("Date: "); mySerial.print(static_cast<int>(month)); mySerial.print("/"); 
    mySerial.print(static_cast<int>(day)); mySerial.print("/"); mySerial.print(year);
  mySerial.print("  Time: "); mySerial.print(static_cast<int>(hour)); mySerial.print(":"); 
    mySerial.print(static_cast<int>(minute)); mySerial.print(":"); mySerial.print(static_cast<int>(second));
    mySerial.print("."); mySerial.print(static_cast<int>(hundredths));
  mySerial.print("  Fix age: ");  mySerial.print(age); mySerial.println("ms.");*/

  mySerial.print("Alt(cm): "); mySerial.print(gps.altitude()); mySerial.print(" Course(10^-2 deg): ");
    mySerial.print(gps.course()); mySerial.print(" Speed(10^-2 knots): "); mySerial.println(gps.speed());
  /*mySerial.print("Alt(float): "); printFloat(gps.f_altitude()); mySerial.print(" Course(float): ");
    printFloat(gps.f_course()); mySerial.println();
  mySerial.print("Speed(knots): "); printFloat(gps.f_speed_knots()); mySerial.print(" (mph): ");
    printFloat(gps.f_speed_mph());
  mySerial.print(" (mps): "); printFloat(gps.f_speed_mps()); mySerial.print(" (kmph): ");
    printFloat(gps.f_speed_kmph()); mySerial.println();

  gps.stats(&chars, &sentences, &failed);
  mySerial.print("Stats: characters: "); mySerial.print(chars); mySerial.print(" sentences: ");
    mySerial.print(sentences); mySerial.print(" failed checksum: "); mySerial.println(failed);*/
}

void printFloat(double number, int digits)
{
  // Handle negative numbers
  if (number < 0.0) {
     Serial.print('-');
     number = -number;
  }

  // Round correctly so that print(1.999, 2) prints as "2.00"
  double rounding = 0.5;
  for (uint8_t i=0; i<digits; ++i)
    rounding /= 10.0;
  
  number += rounding;

  // Extract the integer part of the number and print it
  unsigned long int_part = (unsigned long)number;
  double remainder = number - (double)int_part;
  Serial.print(int_part);

  // Print the decimal point, but only if there are digits beyond
  if (digits > 0)
    Serial.print("."); 

  // Extract digits from the remainder one at a time
  while (digits-- > 0) {
    remainder *= 10.0;
    int toPrint = int(remainder);
    Serial.print(toPrint);
    remainder -= toPrint;
  }
}
