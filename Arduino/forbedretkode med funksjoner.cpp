//#include <Arduino.h>     // kan fjærnes nå Arduino IDE brukes
// Library
#include <Adafruit_AHTX0.h>
#include <CircusESP32Lib.h>
#include <DFRobot_VEML7700.h>

// COT Config
char ssid[] = "Iprobe"; // Name on SSID pede's phone
char psk[] = "Torpedor"; // Password for SSID peder's phone
//char ssid[] = "kameraBad2"; // Name on SSID
//char psk[] = "9D2Remember"; // Password for SSID
char token1[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1Nzk0In0.nqXSqXGe2AXcNm4tdMUl7qIzmpAEXwr7UPKf5AtYx4k"; // COT User
char server[] = "www.circusofthings.com"; // Site communication

// COT Keys
char soilsensor_key1[] = "4991";
char temperature_key1[] = "10571";
char humidity_key1[] = "2615";
char uvsensor_key1[] = "2882";
char luxsensor_key1[] = "17733";
char pump_state_key1[] = "32607";
char ultrasonic_key1[] = "28799";

// Pins
const int soilsensor_pin = 32;
const int uvsensor_pin = 33;
const int echo_pin = 25;
const int trigger_pin = 26;
const int pump_pin = 17;
const int led_pin = 14;

// PWM Config
const int pump_channel = 5;
const int frequency = 1000;
const int resolution = 8;

// Global Variables
volatile int soilsensor_percent;
volatile int uvsensor_percent;
volatile float humidity_value;
volatile float temperature_value;
volatile float lux_value;
volatile float distance_value;
volatile int pump_state;

// Loop Variables
//unsigned long duration;
int distance;
unsigned long pump_duration;

//unsigned long time;
unsigned long pump_start = 0;

Adafruit_AHTX0 aht; 
DFRobot_VEML7700 veml;
CircusESP32Lib circusESP32(server, ssid, psk);
TaskHandle_t Task1;

void setup(){

  //Start communication
  Serial.begin(115200);
  veml.begin();     //starter funksjonen for å lese lysstyrke av Lux sensoren
  aht.begin();      //starter funksjon for å lese temperatur og romfuktighet
  circusESP32.begin();
  
  // pinModes
  pinMode(soilsensor_pin, INPUT);
  pinMode(uvsensor_pin, INPUT);
  pinMode(echo_pin, INPUT);
  pinMode(trigger_pin, OUTPUT);

  //ledC Config
  ledcSetup(pump_channel, frequency, resolution);
  ledcAttachPin(pump_pin, pump_channel);

  // Create a task for Core 0
  xTaskCreatePinnedToCore(
    communication,          // Task Function
    "Task1",                // Name of task (Debug)
    20000,                  // Stack size of task
    NULL,                   // Parameters for task
    2,                      // Priority of the task
    &Task1,                 // Task handle to keep track of created task
    0);                     // Pin task to core 0

}

// Runs in Core 0, and is used for all COT communication
void communication (void * pvParameters){
  for(;;){
    circusESP32.write(soilsensor_key1, soilsensor_percent, token1);
    circusESP32.write(uvsensor_key1, uvsensor_percent, token1);
    circusESP32.write(temperature_key1, temperature_value, token1);
    circusESP32.write(humidity_key1, humidity_value, token1);
    circusESP32.write(luxsensor_key1, lux_value, token1);
    circusESP32.write(ultrasonic_key1, distance_value, token1);

    pump_state = circusESP32.read(pump_state_key1 , token1);
  }
}

int get_soil(int pin){
  int value = analogRead(pin);
  int soilsensor_percent = map(value,0,4095,0,100);    // finner den prosentvise verdien for jordfuktighet
//  int soilsensor_persent = (value/4095)*100;  // finner den prosentvise verdien for jordfuktighet  
  Serial.println(); Serial.print("                Soil Sensor in %: "); Serial.println(soilsensor_percent);
  return soilsensor_percent;
}

int get_uv(int pin){
  int value = analogRead(pin); // denne viser for detmeste 0 men om den får direkte sollys gir den verdier (16.04 kl 14ish ga den 400 ved direkte sollys)
  int uvsensor_persent = map(value,0,611,0,100);         // usikker på nevner verdien, kan være høyere // hyeste målt verdi 1300 20.04 611
//  int uvsensor_persent = (uvsensor_value/611)*100;       // usikker på nevner verdien, kan være høyere
  Serial.print("                UV in %: "); Serial.println(uvsensor_percent);
  return uvsensor_persent;
}

int get_waterlevel(int trig_pin, int echo_pin){    //Ultrasonisk sensor
  unsigned long duration;
  digitalWrite(trig_pin, LOW);
  delayMicroseconds(2);

  digitalWrite(trig_pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig_pin, LOW);
  duration = pulseIn(echo_pin, HIGH);
  int distance_value = duration * 0.034 / 2;
  Serial.print("                Distance: "); Serial.print(distance_value); Serial.println(" cm");

  return distance_value;
  //distance_percent = map(distance_value,0,FYLL iNN,0,100);
}

float get_lux(){
  float lux_value;
 
  veml.getALSLux(lux_value);
  Serial.print("                Lux:"); Serial.print(lux_value); Serial.println(" lx");
  return lux_value;
//  lux_percent = map(lux_value,0,FYLL INN,0,100); // har fått lux = 34 6033.88lx med lys av mobil
}

float get_temp(){
  sensors_event_t humidity,temp;
  aht.getEvent(&humidity, &temp);// populate temp objects with fresh data
  Serial.print("                Temperature: "); Serial.print(temp.temperature); Serial.println(" degrees C");
  temperature_value = temp.temperature;
  return temperature_value;
}

float get_humi(){
  sensors_event_t humidity,temp;
  aht.getEvent(&humidity, &temp);// populate humidity objects with fresh data
  Serial.print("                Humidity: "); Serial.print(humidity.relative_humidity); Serial.println("% rH");

  humidity_value = humidity.relative_humidity;
  return humidity_value;
}

/*
void run_pump(int channel, unsigned long duration, int state, unsigned long start){
  state = 5;
  if (millis() - start < duration) {
    ledcWrite(channel, 150);
  }
  else{
    ledcWrite(channel, 0);
    pump_state = 0;
    update_value()
  }
}

void update_value(char key, int value, char token){
  circusESP32.write(key, value, token);
}
*/

void loop(){
//  time = millis();
  soilsensor_percent = get_soil(soilsensor_pin);
  uvsensor_percent = get_uv(uvsensor_pin);
  distance_value = get_waterlevel(trigger_pin,echo_pin);
  lux_value = get_lux();
  temperature_value = get_temp();
  humidity_value = get_humi();
  
  Serial.println(soilsensor_percent);
  Serial.println(uvsensor_percent);
  Serial.println(distance_value);
  Serial.println(lux_value);
  Serial.println(temperature_value);
  Serial.println(humidity_value);

/*
  switch (pump_state){
  case 1:
    pump_duration = 1000;
      run_pump(pump_channel, pump_duration, pump_state, pump_start);
    pump_start = millis();
    update_value(pump_state_key1, pump_state, token1);
    break;
  
  case 2:
    pump_duration = 2000;
      run_pump(pump_channel, pump_duration, pump_state, pump_start);
    pump_start = millis();
    update_value(pump_state_key1, pump_state, token1);
    break;

  case 3:
    pump_duration = 3000;
      run_pump(pump_channel, pump_duration, pump_state, pump_start);
    pump_start = millis();
    update_value(pump_state_key1, pump_state, token1);
    break;

  case 4:
    pump_duration = 4000;
    run_pump(pump_channel, pump_duration, pump_state, pump_start);
    pump_start = millis();
    update_value(pump_state_key1, pump_state, token1);
    break;

  case 5:
    run_pump(pump_duration);
    update_value(pump_state_key1, pump_state, token1);
    break;

  default:
    pump_state = 0;
    pump_duration = 0;
    break;
  }
*/
  delay(3000);
}

