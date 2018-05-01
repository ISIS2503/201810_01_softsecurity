/*
 * Hertbeat sender
 */
const timeHeart = 60000; 
unsigned long startHeart = millis();    // inicializado en el tiempo actual
unsigned long finishHeart = millis()+timeHeart;	// tiempo final de envio del heartbeat 


// 15 minutos = 900000
// 1 minuto = 60000
void setup() {
 
}
 
void loop(){
	//Si son iguales enviamos la señal
		startHeart = millis();
	if ( startHeart >= finishHeart){
		Serial.println("I'm alive");	
		finishHeart = millis + timeHeart;
	}	
}
