//TODO registrar varias claves (cambiar la estructura por un array

#include <Keypad.h>
/*CONSTANTES KEYPAD*/
//Specified password
#include "WProgram.h"
void setup();
void loop();
void setColor(int redValue, int greenValue, int blueValue);
String KEYS[] = {"1234" , "1111" , "2468", "0811" };
int KEYSLENGTH = 4;

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
  setColor(255,255,0);
  
  // declare LED as output
  pinMode(ledPin, OUTPUT);
  // declare sensor as input
  pinMode(inputPin, INPUT);
}

void loop()
{
  //BATERIA
  //Value conversion from digital to voltage
  batteryCharge = (analogRead(BATTERY_PIN)*3.3)/1024;
  Serial.println(batteryCharge);
  //Measured value comparison with min voltage required
  if(batteryCharge<=MIN_VOLTAGE) {
    digitalWrite(BATTERY_LED,HIGH);
    
  }
  else {
    digitalWrite(BATTERY_LED,LOW);
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
     setColor(255,255,0);
      open = false;
      
      Serial.println("D0");
      digitalWrite(10,LOW);
      currentKey = "";
     
    }
    //If the current key contains '#' reset attempt
    
    if(currentKey.endsWith("#")&&currentKey.length()<=KEYS[0].length()) {
      currentKey = "";
      Serial.println("N0");
    }
  
    //If current key matches the key length
    if (currentKey.length()== KEYS[0].length()) {
      int i = 0;
      boolean bol = false;
      boolean found = false;
      while(i<KEYSLENGTH&&!found){
        String KEY = KEYS[i];
        if(currentKey == KEY) {
          setColor(255,0,255);
          digitalWrite(10,HIGH);
          open = true;
          if(newNumber){
            Serial.println("D1");
            newNumber = false;
          }
          attempts = 0;
          bol = false;
          found = true;
        }
        else {
          bol = true;
        }
        i++;
      }
      found = false;
      if(bol){
        attempts++;
        Serial.println("N"+String(attempts));
        currentKey = "";
        bol = false;
      }
    }else if(currentKey.length()> KEYS[0].length()){
      setColor(255,0,255);
      if(newNumber){
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
      setColor(255,255,0);
      Serial.println("S0");
      
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
      Serial.println("P1");
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
        if(!alertSent){
          Serial.println("P2");
          alertSent = true;
        }
      }
    }else{
      //Blue la puerta esta cerrada y pasa a stand by
      setColor(255,255,0);
      open = false;
      buttonState = false;
      Serial.println("P0");
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
  } else {
    digitalWrite(ledPin, LOW); // turn LED OFF
    if (pirState == HIGH){
      // we have just turned of
      Serial.println("M0");
      // We only want to print on the output change, not state
      pirState = LOW;
    }
  }
  delay(100);
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

