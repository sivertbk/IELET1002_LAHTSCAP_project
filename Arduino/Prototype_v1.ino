// Library
#include <Adafruit_AHTX0.h>
#include <CircusESP32Lib.h>
#include <DFRobot_VEML7700.h>

// COT Config
char ssid[] = "[Insert SSID]"; // Name on SSID
char psk[] = "[Insert password]"; // Password for SSID
char token1[] = "[Insert token]"; // COT User
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

// PWM Config
const int pump_channel = 5;
const int frequency = 1000;
const int resolution = 8;

// Global Variables
volatile int soilsensor_value = 404;
volatile int uvsensor_value;
volatile int pump_state;
volatile float humidity_value;
volatile float temperature_value;
volatile float lux_value;
volatile float distance_value;

// Loop Variables
unsigned long duration;
int distance;

Adafruit_AHTX0 aht;
DFRobot_VEML7700 veml;
CircusESP32Lib circusESP32(server, ssid, psk);
TaskHandle_t Task1;

void setup(){

  //Start communication
  Serial.begin(115200);
  veml.begin();
  aht.begin();
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
void communication( void * pvParameters){
  for(;;){
    soilsensor_value = circusESP32.read(soilsensor_key1, token1);
    Serial.println(soilsensor_value);
  }  
}

void loop(){
  Serial.println(soilsensor_value);
}
