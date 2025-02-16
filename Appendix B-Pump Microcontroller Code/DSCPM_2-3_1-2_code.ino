//Code for the Dual Syringe Continuous Pumping Mechanism (2-3/1-2)
//By BU 2023 iGEM, K. Walp

#include <Servo.h>
#include <math.h>
#include <EEPROM.h>

Servo myservo;
Servo servo;

String incomingByte = "1";

// --------------------------------------------------------- EEPROM Initializers ------------------------------

// Is it your first time uploading this code to an Arduino? UNCOMMENT the next 3 lines :)
int infuse = 1;
int pos = 5; 
int fwd = 0;

// Once you've run the code once and stored your values properly by pausing before turning off, comment these out!

// -------------------------------------------------------- End EEPROM Initializers ---------------------------

// DEFAULT STATE (ON or OFF)
int on = 1; 

// ------------------------------------------------------ EEPROM Statements (Second run and after) ------------

// Comment these out the first time you run your code, or it will not work properly!
//int infuse = EEPROM.read(2);
//int pos = EEPROM.read(0); 
//int fwd = EEPROM.read(1);
////int pos = 15;
// Once you've run your code once and properly stored your values, uncomment these!

// --------------------------------------------------------- End EEPROM Statements ----------------------------


int s1valve = 5; //pin assignments
int s2valve = 6; //pin assignments
int s3valve = 10; //pin assignments NORMALLY ON, IT MUST BE NORMALLY ON!!!!!!!!!!

//int valvestate = 0; // 0 if s1valve is HIGH, 1 if s2valve is HIGH
int valvestate = EEPROM.read(3);

int ODremainder = 100; // overdrive time remainder, reset here and in incrementposition

float amountpumped = 0;

int holdvoltage = 80; //2.35 V, test with your valves.
int maxangle = 70;
int minangle = 5;




// PARAMETERS SET BELOW. READ COMMENTS BEFORE CHANGING ANYTHING.
//------------------------------------------------------------------------
// Inner Diameter of syringes IN MILLIMETERS!
// 0.485mm ID for Hamilton 10µL syringes, but subject to change by user
//
float innerdiameter = 0.485; 
//
//------------------------------------------------------------------------
// Milimeters of Linear Motion per Degree of Rotation from Servo
// 0.256mm for iGEM Linear Servo Actuators V2 (design as of June 15, 2023)
//
float mmperdegree = 0.256;
//
//------------------------------------------------------------------------
// volmultiplier is calculated to take into account that 
// SERVOS DO NOT TURN EXACTLY 180 DEGREES WHEN YOU TELL THEM TO!!!
// Test you servo: write it to 0 degrees, and then to "180" degrees.
// Measure the actual number of degrees that it turns and enter it below:
// Value is 270 for 2023 iGEM GoBilda High Torque Servos
//
float degper180 = 270;
//
float volmultiplier = degper180 / 180.0;
//------------------------------------------------------------------------
// NOTE: One cubic millimeter is one microliter.
//------------------------------------------------------------------------
// For internal use only. Do Not Change.
//
float innerradius = innerdiameter / 2;
float uLperdeg = 3.1415926536 * (innerradius * innerradius) * (mmperdegree * volmultiplier); 
//------------------------------------------------------------------------
// PARAMETERS FINISHED.

//~~~~~~~~~~~~~ SET DEFAULT FLOW RATE BELOW ~~~~~~~~~~~~~~~~~~~
//
float flowrate = 1.5; // µL/min 
//
// DO NOT EXCEED 40 OR THERE WILL BE COMPLICATIONS!!!!!!!!!!!!!!!!!!
//
//~~~~~~~~~~~~~ SET FLOW RATE ABOVE ~~~~~~~~~~~~~~~~~~~~

//----------more params---------------------------------------------------

float minperdeg = uLperdeg / flowrate; // minutes per degree for given flow rate
float millisperdeg = minperdeg * 60000; // milliseconds per degree for given flow rate
int newdelay = int(millisperdeg); // int version of milliseconds per degree to be put in delay

//------------------------------------------------------------------------

void calculatenewdelay(int newflowrate){
  uLperdeg = 3.1415926536 * (innerradius * innerradius) * (mmperdegree * volmultiplier); 
  minperdeg = uLperdeg / flowrate;
  millisperdeg = minperdeg * 60000;
  newdelay = int(millisperdeg);
}

struct posandfwd {
  int pos;
  int fwd;
};

struct posandfwd IncrementPosition(int pos, int fwd, char valvea, char valveb, int infuse, int on){
   if (on == 1){
    if (pos == minangle){
      if (infuse == 0){ 
        valvestate = 1; // b high
      }
      else if (infuse == 1){
        valvestate = 0; // a high
      }
      fwd = 0;
      pos = pos + 1;
      ODremainder = 100;
    }
    else if (pos == maxangle){ // it rips the gears apart if its more than 120 :(
      if (infuse == 0){
        valvestate = 0; // a high
      }
      else if (infuse == 1){
        valvestate = 1; // b high
      }
      fwd = 1;
      pos = pos - 1;
      ODremainder = 100;
    }
    else{ //pos is anything else
      if (fwd == 0){
        pos = pos + 1;
      }
      else if (fwd == 1){
        pos = pos - 1;
      }
    }
  }
  struct posandfwd pos_and_fwd;
  pos_and_fwd.pos = pos;
  pos_and_fwd.fwd = fwd;
  return pos_and_fwd;
}

void overdriveAndDelay(bool remainder, int pos, int valvestate, int newdelay){ // MUST call at each iteration cuz of remainder
  if(remainder){
    //Serial.print("remainder");
    if(ODremainder > newdelay){
      //Serial.print("ODR > ND");
      if(valvestate == 0){
        analogWrite(s1valve, 255);
        analogWrite(s2valve, 0);
      }
      else if(valvestate == 1){
        analogWrite(s1valve, 0);
        analogWrite(s2valve, 255);
      }
      //Serial.println("on1");
      ODremainder = ODremainder - newdelay;
      delay(newdelay);
    }
    else if(ODremainder < newdelay && ODremainder > 0){
      //Serial.print("ODR < ND");
      if(valvestate == 0){
        analogWrite(s1valve, 255);
        analogWrite(s2valve, 0);
        delay(ODremainder);
        analogWrite(s1valve, holdvoltage);
        delay(newdelay - ODremainder);
        ODremainder = 0;
      }
      else if(valvestate == 1){
        analogWrite(s1valve, 0);
        analogWrite(s2valve, 255);
        delay(ODremainder);
        analogWrite(s2valve, holdvoltage);
        delay(newdelay - ODremainder);
        ODremainder = 0;
      }
      //Serial.println("on2");
    }
    else if(ODremainder == 0){
      //Serial.print("ODR = zero");
      delay(newdelay);
    }
  }
  else{ // no remainder
    Serial.print("NO remainder");
    if (pos == minangle || pos == maxangle){
      if (valvestate == 0){ // a high
        analogWrite(s3valve, 255);
        delay(10);
        analogWrite(s1valve, 255);
        analogWrite(s2valve, 0);
        //Serial.println("on1__nana");
        delay(50);
        analogWrite(s3valve, 0);
        delay(100);
        analogWrite(s1valve, holdvoltage);
        //Serial.println("on2__nana");
        delay(newdelay-160);
      }
      else if (valvestate == 1){ // b high
        analogWrite(s3valve, 255);
        delay(10);
        analogWrite(s1valve, 0);
        analogWrite(s2valve, 255);
        //Serial.println("on1__anan");
        delay(50);
        analogWrite(s3valve, 0);
        delay(100);
        analogWrite(s2valve, holdvoltage);
        //Serial.println("on2__anan");
        delay(newdelay-160);
      }
    }
    else{
      /*if (valvestate == 0){ // a high
        analogWrite(s1valve, 70);
        analogWrite(s2valve, 0);
      }
      else if (valvestate == 1){ // b high
        analogWrite(s1valve, 0);
        analogWrite(s2valve, 70);
      }*/
      delay(newdelay);
    }
  }
}

void setup() {
  //solenoid valves setup
  pinMode(s1valve, OUTPUT); //LOW is PUMP, HIGH is REFILL
  pinMode(s2valve, OUTPUT); //LOW is PUMP, HIGH is REFILL

  //servos setup slay
  myservo.attach(9);
  servo.attach(11);
  
  Serial.begin(9600);
}

void loop() {
  // -------------------------------------------TO BE REPLACED WITH I2C RECIEVER STATEMENTS (start)-------------------------------------------
  if (Serial.available() > 0){
    incomingByte = Serial.readString();

    if (incomingByte.toInt() == 0){  //powering system off
      EEPROM.write(0, pos); //------------------------------------------EEPROM------------
      EEPROM.write(1, fwd);
      EEPROM.write(2, infuse);
      EEPROM.write(3, valvestate);
      Serial.print("Position of ");
      Serial.print(pos);
      Serial.println(" degrees saved to EEPROM at index 0");
      on = 0;
    }

    else if (incomingByte.toInt() == 123){ // system on
        on = 1;
        Serial.println("Pumps ON");
    }
    else if (incomingByte.toInt() == 321){ // switch direction OBSOLETE
      if (fwd == 1){
        fwd = 0;
        if (infuse == 0){
          infuse = 1;
        }
        else if (infuse == 1){
          infuse = 0;
        }
      }
      else if (fwd == 0){
        fwd = 1;
        if (infuse == 0){
          infuse = 1;
        }
        else if (infuse == 1){
          infuse = 0;
        }
      }
      Serial.println("Direction Switched");
    }

    else { //chaning flowrate
      flowrate = incomingByte.toInt();
      calculatenewdelay(flowrate);

      Serial.print("Flow Rate Changed to ");
      Serial.print(flowrate);
      Serial.println(" µL/min");
    }
  }

  // -------------------------------------------TO BE REPLACED WITH I2C RECIEVER STATEMENTS (end)-------------------------------------------

  struct posandfwd posandfwd_ = IncrementPosition(pos, fwd, s1valve, s2valve, infuse, on);
  pos = posandfwd_.pos;
  fwd = posandfwd_.fwd;

  if (on == 1){
    if (infuse == 0){
      amountpumped = amountpumped + uLperdeg;
    }
    else if (infuse == 1){
      amountpumped = amountpumped - uLperdeg;
    }
  }

  myservo.write(pos);
  Serial.print(pos);
  Serial.print(", ");
  Serial.print(amountpumped);
  Serial.print(" µL, ");

  if (newdelay >= 100){
    overdriveAndDelay(false, pos, valvestate, newdelay);
  }
  else if (newdelay < 100){
    overdriveAndDelay(true, pos, valvestate, newdelay);
  }
  
  Serial.println(newdelay);

}
