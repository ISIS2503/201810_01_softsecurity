//TODO registrar varias claves (cambiar la estructura por un array

#include <Keypad.h>
/*CONSTANTES KEYPAD*/
//Specified password
const String KEY = "1234";

//Time in milliseconds which the system is locked
const int LOCK_TIME = 30000;

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

void setup()
{
  Serial.begin(9600);
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
}

void loop()
{
  //KEYPAD  
  char customKey;
   if(!block) {
      //Selected key parsed;
      customKey = customKeypad.getKey();
    }
    else {
      setColor(0,255,255);
      Serial.println("Number of attempts exceeded");
      while(true);

    }
  
    //Verification of input and appended value
    if (customKey) {  
      currentKey+=String(customKey);
      Serial.println(currentKey);
    }
  
    //If the current key contains '*' and door is open
    if(open && currentKey.endsWith("*")) {
     setColor(255,255,0)
      open = false;
      
      Serial.println("Door closed");
      digitalWrite(10,LOW);
      currentKey = "";
     
    }
    //If the current key contains '#' reset attempt
    if(currentKey.endsWith("#")&&currentKey.length()<=KEY.length()) {
      currentKey = "";
      Serial.println("Attempt deleted");
    }
  
    //If current key matches the key length
    if (currentKey.length()== KEY.length()) {
      if(currentKey == KEY) {
        setColor(255,0,255)
        digitalWrite(10,HIGH);
        open = true;
        Serial.println("Door opened!!");
        attempts = 0;
        
      }
      else {
        attempts++;
        currentKey = "";
        Serial.println("Number of attempts: "+String(attempts));
      }
    }else if(currentKey.length()> KEY.length()){
      setColor(255,0,255)
      Serial.println("Door opened!!");
    }
    if(attempts>=maxAttempts) {
      setColor(255,255,0)
      currentKey = "";
      attempts = 0;
      Serial.println("System locked");
      
      delay(LOCK_TIME);
      setColor(255,0,255)
      Serial.println("System unlocked");
      
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
      Serial.println("Se abrio la puerta, se reiniciaron los intentos.");
    }
  }
  else {
    if(digitalRead(CONTACT_PIN)) {
      //Tiempo de apertura mayor a 30 segundos
      if((millis()-currTime)>=30000) {
        setColor(0, 255, 255);
        Serial.println("puerta abierta mas de 30 segundos");
      }
    }else{
      //Blue la puerta esta cerrada y pasa a stand by
      setColor(255,255,0);
      open = false;
      buttonState = false;
      Serial.println("Puerta cerrada!!");
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
