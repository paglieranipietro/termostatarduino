#include <DHT11.h>
#include <ArduinoJson.h>
#include <ArduinoJson.hpp>
 
DHT11 sensore(2);
#define LED1 6
#define LED2 7
const int SOGLIA_MINIMA = 15;
const int SOGLIA_MASSIMA = 25;

unsigned long startTime;
void setup() {
  Serial.begin(9600);
  pinMode(LED1 , OUTPUT);
  pinMode(LED2 , OUTPUT);
 
  startTime = millis();
}
 
const int SEND_INTERVAL = 2000;
StaticJsonDocument<200> jsonBuffer;
void loop() {
    int temp = 0;
    int umidita = 0;
    bool led1 = false, led2 = false;
 
    unsigned long elapsedTime = millis() - startTime;
 
    int result = sensore.readTemperatureHumidity(temp, umidita);
    if(temp >= SOGLIA_MINIMA && temp <= SOGLIA_MASSIMA){
      digitalWrite(LED1,HIGH);
      digitalWrite(LED2,LOW);
      led1=true;
      led2=false;
    }else if(temp > SOGLIA_MASSIMA){
      digitalWrite(LED2, HIGH);
      digitalWrite(LED1, LOW);
      led2=true;
      led1=false;
    }else if(temp < SOGLIA_MINIMA){
      digitalWrite(LED2, LOW);
      digitalWrite(LED1, LOW);
      led2=false;
      led1=false;
    }
 
    if (elapsedTime > SEND_INTERVAL) {
      startTime = millis();
      if (result == 0) {
        jsonBuffer["temp"] = temp;
        jsonBuffer["umid"] = umidita;
        jsonBuffer["led1"] = led1;
        jsonBuffer["led2"] = led2;
      } else {
        jsonBuffer["error"] = true;
      }
 
      sendData(jsonBuffer);
    }
 
}
 
void sendData(StaticJsonDocument<200> &jBuff){
  if (jBuff.isNull())
    return;
  serializeJson(jBuff, Serial); // Serializza il buffer JSON e lo invia sulla seriale
  Serial.println(); // Aggiunge un newline alla fine del messaggio
 
  jBuff.clear(); // Pulisce il buffer JSON per il prossimo utilizzo
}
