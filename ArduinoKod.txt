// Dasduino connect plus (ljubicasti)  // Arduinu MKR1000 (plavi)
//#include<ESP32Servo.h>               // #include<Servo.h> 
#define LED_PIN 4                      // #define LED_PIN 4
#define TEMP_PIN 32                    // #define TEMP_PIN A0
#define ANALOG_RANGE 4095.0            // #define ANALOG_RANGE 4095.0

//Servo servo;

void setup() {
  pinMode(LED_PIN, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  if(Serial.available() > 0) {
    int num = Serial.read() - '0';
    
    switch (num) {
      case 0:
        digitalWrite(LED_PIN, LOW);
        break;
      case 1:
        digitalWrite(LED_PIN, HIGH);
        break;
      case 2: {
        int analogValue = analogRead(TEMP_PIN);  // vrijednost od 0-1024 koja odgovara naponu od 0-3.3V
        float voltage = analogValue * 3.3 / ANALOG_RANGE;  // pretvaramo ocitanu vrijednost u napon
        //  pretvorba napona u stupnjeve Celzijuse:
        //  0.5V odgovara temperaturi od 0°C, a svaki volt odgovara rasponu od 100°C
        int deg = round((voltage - 0.5) * 100.0);
        Serial.println(deg);

        break;
      }
      case 3:
        break;
      case 4:
        break;
    }
  }
}
