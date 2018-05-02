#include <PubSubClient.h>
#include <ESP8266WiFi.h>

//DEFINES
#define TOPIC_SUBSCRIBE        "conjunto1/residencia1/cerradura"
#define TOPIC_PUBLISH          "conjunto1/residencia1/alerta"
#define SIZE_BUFFER_DATA       50

//VARIABLES
const char* idDevice = "ISIS2503";
boolean     stringComplete = false;
boolean     init_flag = false;
String      inputString = "";
char        bufferData [SIZE_BUFFER_DATA];

// CLIENTE WIFI & MQTT
WiFiClient    clientWIFI;
PubSubClient  clientMQTT(clientWIFI);

// CONFIG WIFI
//u:EventosUAndes c:EvUniandinos.18
const char* ssid = "EventosUAndes";
const char* password = "EvUniandinos.18";

// CONFIG MQTT
const char* mqtt_server = "broker.mqtt-dashboard.com";
IPAddress serverMQTT (172,24,42,37);
const uint16_t portMQTT = 1883;

// const char* usernameMQTT = "admin";
// const char* passwordMQTT = "admin";

void connectWIFI() {
  // Conectar a la red WiFi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  if(WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
  }

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println(WiFi.localIP());
}

void reconnectWIFI() {
  // Conectar a la red WiFi
  if(WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
  }

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.write(payload, length);
  Serial.println();
  }

void setup() {
  Serial.begin(9600);
  inputString.reserve(100);
  clientMQTT.setServer(mqtt_server, 1883);
  //clientMQTT.setServer(serverMQTT, portMQTT);
  clientMQTT.setCallback(callback);
  connectWIFI();
  delay(1000);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  
}

void processData() {
      
  if (WiFi.status() == WL_CONNECTED) {
    if(init_flag == false) {
      init_flag = true;

      boolean conectMQTT = false;
      if (!clientMQTT.connected()) {
        // if (!clientMQTT.connect(idDevice, usernameMQTT, passwordMQTT)) {
        if (!clientMQTT.connect(idDevice)) {
          conectMQTT = false;
        }
        conectMQTT = true;
      }
      else {
        conectMQTT = false;
      }

      if(conectMQTT) {
        if(clientMQTT.subscribe(TOPIC_SUBSCRIBE)) {
          Serial.println("Subscribe OK");
          digitalWrite(LED_BUILTIN, LOW);
          
        }
      }
    }

    if (stringComplete && clientMQTT.connected()) {
      if(clientMQTT.publish(TOPIC_PUBLISH, bufferData)) {
        inputString = "";
        stringComplete = false;
      }
      init_flag = false;
    }
  }
  else {
    connectWIFI();
    init_flag = false;
  }
  //Serial.print(clientMQTT.state());
  clientMQTT.loop();
}

void receiveData() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      inputString.toCharArray(bufferData, SIZE_BUFFER_DATA);
      stringComplete = true;
    }
  }
}

void loop() {
  receiveData();
  processData();
}
