#include <Braccio.h>
#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_ver;
Servo wrist_rot;
Servo gripper;

//Constants and variables to hold input from the serial port
int keysIndex = 0;
const int KEYS = 12;
int input[KEYS] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

//Constants and variables to hold the angles of the motors
const int MOTORS = 6;
                  //{M1,M2,  M3,  M4, M5, M6}
int angle[MOTORS] = {0 , 45, 180, 180, 90, 90};

//Constant to control the angle increment when pressing a key
const int increment = 25;

void setup() {
  //De-activate Braccio´s soft start
  pinMode(12, OUTPUT);
  digitalWrite(12, HIGH);
  Braccio.begin(SOFT_START_DISABLED);

  //Setup the serial port
  Serial.begin(9600);
}

void loop() {
  //Read the input from Processing through the serial port:
  if (Serial.available() > 0) {
    char ch = Serial.read();

    //Read fields between comas(,):
    if (ch == '0' || ch == '1') {
      input[keysIndex] = (ch - '0');
    }
    else if (ch == ',') {             //if it is a coma(,) then change field
      if (keysIndex < KEYS - 1) {
        keysIndex++;
      }
    }
    else if (ch == '\n') {           //if it is a line feed(\n) then end read.

      //For each field in the input array, evaluate if it is a 0 or a 1 and midify the angles of the motors
      for (int e = 0; e <= KEYS - 1; e++) {
        switch (e) {
          case 0:                               // M1 clockwise: RIGHT
            if (input[e] == 1) {
              angle[0] = angle[0] + increment;
              if (angle[0] > 180) {
                angle[0] = 180;
              }
            }
            break;
          case 1:                               // M1 counterclockwise: LEFT
            if (input[e] == 1) {
              angle[0] = angle[0] - increment;
              if (angle[0] < 0) {
                angle[0] = 0;
              }
            }
            break;
          case 2:                               // M2 front tilt: UP
            if (input[e] == 1) {
              angle[1] = angle[1] + increment;
              if (angle[1] > 165) {
                angle[1] = 165;
              }
            }
            break;
          case 3:                               // M2 back tilt: DOWN
            if (input[e] == 1) {
              angle[1] = angle[1] - increment;
              if (angle[1] < 15) {
                angle[1] = 15;
              }
            }
            break;
          case 4:                               // M3 front tilt: D
            if (input[e] == 1) {
              angle[2] = angle[2] + increment;
              if (angle[2] > 180) {
                angle[2] = 180;
              }
            }
            break;
          case 5:                               // M3 back tilt: A
            if (input[e] == 1) {
              angle[2] = angle[2] - increment;
              if (angle[2] < 0) {
                angle[2] = 0;
              }
            }
            break;
          case 6:                              // M4 front tilt: W
            if (input[e] == 1) {
              angle[3] = angle[3] + increment;
              if (angle[3] > 180) {
                angle[3] = 180;
              }
            }
            break;
          case 7:                             // M4 back tilt: S
            if (input[e] == 1) {
              angle[3] = angle[3] - increment;
              if (angle[3] < 0) {
                angle[3] = 0;
              }
            }
            break;
          case 8:                            // M5 clockwise: E
            if (input[e] == 1) {
              angle[4] = angle[4] + increment;
              if (angle[4] > 180) {
                angle[4] = 180;
              }
            }
            break;
          case 9:                            // M5 clokwise: Q
            if (input[e] == 1) {
              angle[4] = angle[4] - increment;
              if (angle[4] < 0) {
                angle[4] = 0;
              }
            }
            break;
          case 10:                           // M6 grip close: Ctrl
            if (input[e] == 1) {
              angle[5] = angle[5] + increment;
              if (angle[5] > 127) {
                angle[5] = 127;
              }
            }
            break;
          case 11:                           // M6 grip open: Shift
            if (input[e] == 1) {
              angle[5] = angle[5] - increment;
              if (angle[5] < 52) {
                angle[5] = 52;
              }
            }
            break;
        }
      }
      //Write the new angles to the motors
                         //(step delay,M1       ,M2       ,M3       , M4      , M5      , M6      );
      Braccio.ServoMovement(20        , angle[0], angle[1], angle[2], angle[3], angle[4], angle[5]);
    }
    keysIndex=0;
  }
}
