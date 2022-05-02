#include <Braccio.h>
#include <Servo.h>

#define LEFT 97 //a
#define RIGHT 115 //s

#define M1 49 //1
#define M2 50
#define M3 51
#define M4 52
#define M5 53
#define M6 54 //6
#define NONE 0 //stop

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

int activeMotor = NONE;

//Initial Value for each Motor
int m1 = 150;
int m2 = 17;
int m3 = 83;
int m4 = 180;
int m5 = 60;
int m6 = 60;


void setup()
{
  Braccio.begin();
  Serial.begin(9600);
  Braccio.ServoMovement(20, 0,  m2, m3, m4, m5,  m6); //step to avoid wall
  Braccio.ServoMovement(20, m1,  m2, m3, m4, m5,  m6);
  Serial.println("Set up done");
}

void loop()
{
     /*
   Step Delay: a milliseconds delay between the movement of each servo.  Allowed values from 10 to 30 msec.
   M1=base degrees. Allowed values from 0 to 180 degrees
   M2=shoulder degrees. Allowed values from 15 to 165 degrees
   M3=elbow degrees. Allowed values from 0 to 180 degrees
   M4=wrist vertical degrees. Allowed values from 0 to 180 degrees
   M5=wrist rotation degrees. Allowed values from 0 to 180 degrees
   M6=gripper degrees. Allowed values from 10 to 73 degrees. 10: the toungue is open, 73: the gripper is closed.
  */

  if (Serial.available()) {

    char InChar = Serial.read();
    int input = InChar;
    
    if (input>=49 && input<=54) { 
      
      activeMotor=input;
      Serial.println("Selected Motor");
      Serial.println(InChar);
      Serial.println("\n");
    }

    else if (input ==55) {
      
      Serial.println(m1);
      Serial.println(m2);
      Serial.println(m3);
      Serial.println(m4);
      Serial.println(m5);
      Serial.println(m6);
 
      }
    
    else {
      
      switch (activeMotor) {
            case M1:
                if (input==RIGHT) {
                  m1=m1+1;
                  base.write(m1);
                  }
                 else if (input==LEFT) {
                  m1=m1-1;
                  base.write(m1);
                  }
                if(m1>180){m1=180;}
                if(m1<0){m1=0;}
                break;
                
              case M2:
                if (input==RIGHT) {
                  m2=m2+1;
                  shoulder.write(m2);
                  }
                 else if (input==LEFT) {
                  m2=m2-1;
                  shoulder.write(m2);
                  }
                  if(m2>165){m2=165;}
                  if(m2<15){m2=15;}
                break;

               case M3:
                if (input==RIGHT) {
                  m3=m3+1;
                  elbow.write(m3);
                  }
                 else if (input==LEFT) {
                  m3=m3-1;
                  elbow.write(m3);
                  }
                  if(m3>180){m3=180;}
                  if(m3<0){m3=0;}
                
                break;

              case M4:
                if (input==RIGHT) {
                  m4=m4+1;
                  wrist_rot.write(m4);
                  }
                 else if (input==LEFT) {
                  m4=m4-1;
                  wrist_rot.write(m4);
                  }
                  if(m4>180){m4=180;}
                  if(m4<0){m4=0;}
                  
                break;
                
               case M5:
                if (input==RIGHT) {
                  m5=m5+20;
                  wrist_ver.write(m5);
                  }
                 else if (input==LEFT) {
                  m5=m5-20;
                  wrist_ver.write(m5);
                  }
                  if(m5>180){m5=180;}
                  if(m5<0){m5=0;}
                  
                break;

               case M6:
                if (input==RIGHT) {
                  m6=m6+70;
                  gripper.write(m6);
                  }
                 else if (input==LEFT) {
                  m6=m6-70;
                  gripper.write(m6);
                  }
                  if(m6>73){m6=73;}
                  if(m6<10){m6=10;}
                  
                break;

                
             case NONE:
                Serial.println("First select a motor. \n");
                break; 

                
            default:
                printf("Out of range");
                break;
        }

      
    }

  }
  
  //Wait 1 second
  delay(1000);

}
