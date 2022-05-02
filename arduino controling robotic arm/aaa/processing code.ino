/* BraccioKeyboardController v3.1
*/

//Import serial library and declare serial name
import processing.serial.*;
Serial myPort;

//Variables:
int keys=12;
                  //{0    ,1    ,2    ,3    ,4    ,5    ,6    ,7    ,8    ,9    ,10   ,11   }
                  //{RIGHT,LEFT ,UP   ,DOWN ,D    ,A    ,W    ,S    ,E    ,Q    ,CTRL ,SHIFT}
int keyStatus[]={0,0,0,0,0,0,0,0,0,0,0,0};

void setup(){
  size(100,100);
  
  //Setup the serial port
  String portName = Serial.list()[0];
  myPort = new Serial(this, portName, 9600);
}

void draw(){
  background(0,0,0);
  //Write the values of the keyStatus on the serial port and print the values so I can see it.
  for(int i=0; i<=keys-1; i++){
    myPort.write(keyStatus[i]);
    print(keyStatus[i]);
    if(i<keys-1){
      myPort.write(',');
      print(',');
    }
    if(i==keys-1){
      myPort.write('\n');
      println();
    }
  }
}

void keyPressed() {
  //Read the pressed keys and assign value 1 to indicate the the key is pressed
  if (key==CODED){
    if(keyCode==RIGHT){keyStatus[0]=1;}
    if(keyCode==LEFT){keyStatus[1]=1;}
    if(keyCode==UP){keyStatus[2]=1;}
    if(keyCode==DOWN){keyStatus[3]=1;}
    if(keyCode==CONTROL){keyStatus[10]=1;}
    if(keyCode==SHIFT){keyStatus[11]=1;}
  }
  else{
    if(key=='d'){keyStatus[4]=1;}
    if(key=='a'){keyStatus[5]=1;}
    if(key=='w'){keyStatus[6]=1;}
    if(key=='s'){keyStatus[7]=1;}
    if(key=='e'){keyStatus[8]=1;}
    if(key=='q'){keyStatus[9]=1;}
  }
}

void keyReleased(){
  //Read the pressed keys and assign value 0 to indicate the the key is pressed
  if (key==CODED){
    if(keyCode==RIGHT){keyStatus[0]=0;}
    if(keyCode==LEFT){keyStatus[1]=0;}
    if(keyCode==UP){keyStatus[2]=0;}
    if(keyCode==DOWN){keyStatus[3]=0;}
    if(keyCode==CONTROL){keyStatus[10]=0;}
    if(keyCode==SHIFT){keyStatus[11]=0;}
  }
  else{
    if(key=='d'){keyStatus[4]=0;}
    if(key=='a'){keyStatus[5]=0;}
    if(key=='w'){keyStatus[6]=0;}
    if(key=='s'){keyStatus[7]=0;}
    if(key=='e'){keyStatus[8]=0;}
    if(key=='q'){keyStatus[9]=0;}
  }
}
