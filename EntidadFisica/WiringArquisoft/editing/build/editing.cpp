//TODO registrar varias claves (cambiar la estructura por un array

#include <Keypad.h>
#include <EEPROM.h>
/*
 * Hertbeat sender
 */
#include "WProgram.h"
void setup();
void loop();
void setColor(int redValue, int greenValue, int blueValue);
boolean compareKey(String key);
void processCommand(String command);
void addPassword(int val, int index);
void updatePassword(int val, int index);
void deletePassword(int index);
void deleteAllPasswords();
void recoverPassword(int index);
const unsigned long timeHeart = 60000; 
unsigned long startHeart = millis();    // inicializado en el tiempo actual
unsigned long finishHeart = millis()+timeHeart;	// tiempo final de envio del heartbeat 

//constantes de comandos
const int ADD=0;
const int UPDATE=1;
const int DELETE = 2;
const int DELETEALL=3;
const int RECOVER=4;

/*CONSTANTES KEYPAD*/
//Key size
const int KEYSIZE = 4;

//Time in milliseconds which the system is locked
const int LOCK_TIME = 1000;

//Keypad rows
const byte ROWS = 4; 

//Keypad columns
const byte COLS = 3;

//Maximum number of attempts allowed
const byte maxAttempts = 3;

//Keypad mapping matrix
char hexaKeys[ROWS][COLS] = {
  {
    '1', '2', '3'
  }
  ,
  {
    '4', '5', '6'
  }
  ,
  {
    '7', '8', '9'
  }
  ,
  {
    '*', '0', '#'
  }
};

//PINES DEL KEYPAD
//Keypad row pins definition 
byte rowPins[ROWS] = {
  9, 8, 7, 6
}; 

//Keypad column pins definition
byte colPins[COLS] = {
  5, 4, 3
};

//Current key variable
String currentKey;

//Keypad library initialization
Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

//If the number of current attempts exceeds the maximum allowed
boolean block;

/*CONSTANTES LED RGB*/
//Button pin
const int CONTACT_PIN = 11;

//R LED pin
const int R_LED_PIN = 13;

//G LED pin
const int G_LED_PIN = 12;

//B LED pin
const int B_LED_PIN = 10;

//Door state
boolean open;

//Attribute that defines the button state
boolean buttonState;

/*Generales*/
//Current time when the button is tapped
long currTime;

//Number of current attempts
byte attempts;

/* PIR sensor tester */
// choose the pin for the LED
int ledPin = 14;
// choose the input pin (for PIR sensor)
int inputPin = 2; 
// we start, assuming no motion detected
int pirState = LOW;
// variable for reading the pin status
int val = 0;

boolean newNumber = false;
boolean alertSent = false;

/*ALARMA BATERIA*/
//Minimum voltage required for an alert
const double MIN_VOLTAGE = 1.2;

//Battery measure pin
const int BATTERY_PIN = 24;

//Battery indicator
const int BATTERY_LED = 15;

//Current battery charge
double batteryCharge;

boolean pause = false;
unsigned long time1 = millis();
unsigned long time2 = millis();
boolean initsound = true;
void setup()
{
  Serial.begin(9600);

  //BATERIA

  // Ouput pin definition for BATTERY_LED
  pinMode(BATTERY_LED,OUTPUT);

  //Input pin definition for battery measure
  pinMode(BATTERY_PIN,INPUT);


  //KEYPAD
  currentKey = "";
  open = false;
  attempts = 0;
  block = false;

  //RGBLED
  buttonState = false;

  pinMode(R_LED_PIN, OUTPUT);
  pinMode(G_LED_PIN, OUTPUT);
  pinMode(B_LED_PIN, OUTPUT);
  pinMode(CONTACT_PIN,INPUT);
  // inicia con color azul STANDBY
  setColor(191,191,0);

  // declare LED as output
  pinMode(ledPin, OUTPUT);
  // declare sensor as input
  pinMode(inputPin, INPUT);
}

void loop()
{
	
//Si son iguales enviamos la se\u00f1al
		startHeart = millis();
	if ( startHeart >= finishHeart){
		Serial.println("I'm alive");	
		finishHeart = millis() + timeHeart;
	}	
	
	
  //BATERIA
  //Value conversion from digital to voltage
  batteryCharge = 1000;//(analogRead(BATTERY_PIN)*3.3)/1024;
  //Serial.println(analogRead(BATTERY_PIN)*100);

  //Measured value comparison with min voltage required
  if(batteryCharge<=MIN_VOLTAGE) {
    digitalWrite(BATTERY_LED,HIGH);

    time1 = millis();
    if(!pause) {
      time2 = millis()+30000;
      pause=true;
    }
    if(time2<time1 || initsound) {
      tone(16, 262);
      Serial.println("sound");
      delay(2000);
      noTone(16);
      pause=false;
      time1=millis();
      time2=millis();
      initsound = false;
      //Serial.println("B0");
    }
  }
  else {
    digitalWrite(BATTERY_LED,LOW);
    initsound = true;
  }

  //KEYPAD  
  char customKey;
  //Selected key parsed;
  customKey = customKeypad.getKey();

  //Verification of input and appended value
  if (customKey) {  
    currentKey+=String(customKey);
    Serial.println(currentKey);
    newNumber = true;
  }

  //If the current key contains '*' and door is open
  if(open && currentKey.endsWith("*")) {
    setColor(191,191,0);
    open = false;

    //Serial.println("D0");
    digitalWrite(10,LOW);
    currentKey = "";
  }
  //If the current key contains '#' reset attempt

  if(currentKey.endsWith("#")&&currentKey.length()<=KEYSIZE) {
    currentKey = "";
    //Serial.println("N0");
  }

  //If current key matches the key length
  if (currentKey.length()== KEYSIZE) {
    int i = 0;
    boolean bol = false;
    boolean found = false;
    if(compareKey(currentKey)) {
      setColor(255,0,255);
      digitalWrite(10,HIGH);
      open = true;
      if(newNumber) {
        //Serial.println("D1");
        newNumber = false;
      }
      attempts = 0;
      bol = false;
      found = true;
    }
    else {
      bol = true;
    }
    found = false;
    if(bol) {
      attempts++;
      //Serial.println("N"+String(attempts));
      currentKey = "";
      bol = false;
    }
  }
  else if(currentKey.length()> KEYSIZE) {
    setColor(255,0,255);
    if(newNumber) {
      Serial.println("D1");
      newNumber = false;
    }
  }
  if(attempts>=maxAttempts) {
    setColor(0,255,255);
    currentKey = "";
    attempts = 0;
    Serial.println("S1");

    tone(16, 262);
    delay(LOCK_TIME);
    noTone(16);
    setColor(191,191,0);
    //Serial.println("S0");
  }

  delay(100);   





  //RGBLED
  //Button input read and processing 
  if(!buttonState) {
    if(digitalRead(CONTACT_PIN)) {
      currTime = millis();
      buttonState = true;
      setColor(255,0,255);
      open = true;
      attempts = 0;
      //Serial.println("P1");
    }
  }
  else {
    if(digitalRead(CONTACT_PIN)) {
      //Tiempo de apertura mayor a 30 segundos
      if((millis()-currTime)>=5000) {
        setColor(0, 255, 255);
        tone(16, 1047);
        delay(500);
        noTone(16);
        tone(16, 523);
        delay(500);
        noTone(16);
        if(!alertSent) {
          Serial.println("P2");
          alertSent = true;
        }
      }
    }
    else {
      //Blue la puerta esta cerrada y pasa a stand by
      setColor(191,191,0);
      open = false;
      buttonState = false;
      //Serial.println("P0");
      alertSent = false;
    }
  }
  delay(100);


  //PIR sensor
  // read input value
  val = digitalRead(inputPin);
  // check if the input is HIGH  
  if (val == HIGH) {      
    // turn LED ON    
    digitalWrite(ledPin, HIGH);  
    if (pirState == LOW) {
      // we have just turned on
      Serial.println("M1");
      // We only want to print on the output change, not state
      pirState = HIGH;
    }
  } 
  else {
    digitalWrite(ledPin, LOW); // turn LED OFF
    if (pirState == HIGH) {
      // we have just turned of
      //Serial.println("M0");
      // We only want to print on the output change, not state
      pirState = LOW;
    }
  }
  delay(100);
  //leer de la wifi
  
  String inputString = "";
  while(Serial.available()) {
    char inChar;
    inChar = char(Serial.read());
    Serial.println(inputString);
    if(char(inChar) == '\n') {
      processCommand(inputString);
    }
    inputString += String(inChar);
  }
}

//Method that outputs the RGB specified color
void setColor(int redValue, int greenValue, int blueValue) {

  //RED COLOR (0,255,255)
  //GREEN COLOR (255,0,255)
  //BLUE COLOR (255,255,0)

  analogWrite(R_LED_PIN, redValue);
  analogWrite(G_LED_PIN, greenValue);
  analogWrite(B_LED_PIN, blueValue);
}


// Method that compares a key with stored keys
boolean compareKey(String key) {
  int acc = 3;
  int codif, arg0, arg1; 
  for(int i=0; i<3; i++) {
    codif = EEPROM.read(i);
    while(codif!=0) {
      if(codif%2==1) {
        arg0 = EEPROM.read(acc);
        arg1 = EEPROM.read(acc+1)*256;
        arg1+= arg0;
        if(String(arg1)==key) {
          return true;
        }
      }
      acc+=2;
      codif>>=1;
    }
    acc=(i+1)*16+3;
  }
  return false;
}

// Method that divides the command by parameters
void processCommand(String command) {
  Vector <int> comNum;
  splitString(command, ';', comNum);

  if(comNum.get(0)==ADD) {
    addPassword(comNum.get(1),comNum.get(2));
    Serial.println(comNum.get(1));
    Serial.println(comNum.get(2));
    Serial.print("add");
  }
  else if(comNum.get(0)==UPDATE) {
    updatePassword(comNum.get(1),comNum.get(2));
    Serial.print("update");
  }
  else if(comNum.get(0)==DELETE) {
    deletePassword(comNum.get(1));
    Serial.print("delete");
  }
  else if(comNum.get(0)==DELETEALL) {
    deleteAllPasswords();
    Serial.print("deleteall");
  }
  else if(comNum.get(0) == RECOVER) {
	recoverPassword(comNum.get(1));
	Serial.print("recover");
  }
}

//Method that adds a password in the specified index
void addPassword(int val, int index) {
  byte arg0 = val%256;
  byte arg1 = val/256;
  EEPROM.write((index*2)+3,arg0);
  EEPROM.write((index*2)+4,arg1);
  byte i = 1;
  byte location = index/8;
  byte position = index%8;
  i<<=position;
  byte j = EEPROM.read(location);
  j |= i;
  EEPROM.write(location,j);
}

//Method that updates a password in the specified index
void updatePassword(int val, int index) {
  byte arg0 = val%256;
  byte arg1 = val/256;
  EEPROM.write((index*2)+3,arg0);
  EEPROM.write((index*2)+4,arg1);
}

//Method that deletes a password in the specified index
void deletePassword(int index) {
  byte i = 1;
  byte location = index/8;
  byte position = index%8;
  i<<=position;
  byte j = EEPROM.read(location);
  j ^= i;
  EEPROM.write(location,j);
}

//Method that deletes all passwords
void deleteAllPasswords() {
  //Password reference to inactive
  EEPROM.write(0,0);
  EEPROM.write(1,0);
  EEPROM.write(2,0);
}

//Method that recovers a password
void recoverPassword(int index) {
  byte i = 1;
  byte location = index/8;
  byte position = index%8;
  i<<=position;
  byte j = EEPROM.read(location);
  j |= i;
  EEPROM.write(location,j);
}


