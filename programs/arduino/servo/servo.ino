#include <Servo.h>


//List of the different pins and their linked servo
//pin 6 - opening/closing of the grabber
//pin 5 - rotating upper arm part
//pin 2 - rotating base of arm
//pin 3 - rotating lower arm part


  // create servo object to control a servo
Servo myservo2;
Servo myservo3;
  
int potpin = 0;  // analog pin used to connect the potentiometer
int val;    // variable to read the value from the analog pin

void setup() {
  // attaches the servo on pin 9 to the servo object
  myservo2.attach(6); 
  myservo3.attach(5);
}

void loop() {
  val = analogRead(potpin);            // reads the value of the potentiometer (value between 0 and 1023)
  val = map(val, 0, 1023, 0, 180);     // scale it to use it with the servo (value between 0 and 180)
                // sets the servo position according to the scaled value
   myservo2.write(0); 
   myservo3.write(100); 
  delay(1500);                           // waits for the servo to get there                  // sets the servo position according to the scaled value
   myservo2.write(100);
   myservo3.write(0);
  delay(1500);  

}
