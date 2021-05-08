// Library
#include <Adafruit_AHTX0.h>
#include <CircusESP32Lib.h>
#include <DFRobot_VEML7700.h>
#include <SPI.h>            // library for configuration of OLED display
#include <TFT_eSPI.h>       // Hardware-specific library

TFT_eSPI tft = TFT_eSPI();  // Invoke custom library

#define num_readings 12
#define sleep_time 22
#define second 1000000         // converts micro seconds to seconds
#define pump_magnitude 255     // Constant to say how fast the pump should run when it is running (given in 8 bits)
#define led_brightness 150
#define Threshold 40           // Greater the value, more the sensitivity on touchpin

// COT Config
char ssid[] = "kameraBad2"; // Name on SSID
char psk[] = "9D2Remember"; // Password for SSID
char token1[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1Nzk0In0.nqXSqXGe2AXcNm4tdMUl7qIzmpAEXwr7UPKf5AtYx4k"; // COT User
char server[] = "www.circusofthings.com"; // Site communication

// Plant (THis is important if there are more plants connected to the same RPI)
const int plant = 1;

// COT Keys
char state_array1_key[] = "23560";

char soilsensor_key1[] = "4991";
char temperature_key1[] = "10571";
char humidity_key1[] = "2615";
char uvsensor_key1[] = "2882";
char luxsensor_key1[] = "17733";
char ultrasonic_key1[] = "28799";

// Pins
const int soilsensor_pin = 32;
const int uvsensor_pin = 33;
const int echo_pin = 25;
const int trigger_pin = 26;
const int pump_pin = 17;
const int led_pin = 14;

// PWM constants
const int pump_channel = 5;
const int led_channel = 6;

const int frequency = 5000;
const int resolution = 8;


// Counter to track how many times ESP32 has awaken form its deep sleep
RTC_DATA_ATTR int boot_counter = 0;

// Value Variables
RTC_DATA_ATTR float soil[num_readings];
RTC_DATA_ATTR float uv[num_readings];
RTC_DATA_ATTR float humidity[num_readings];
RTC_DATA_ATTR float temperature[num_readings];
RTC_DATA_ATTR float lux[num_readings];
RTC_DATA_ATTR float distance[num_readings];

RTC_DATA_ATTR float last_soil_val;
RTC_DATA_ATTR float last_uv_val;
RTC_DATA_ATTR float last_humidity_val;
RTC_DATA_ATTR float last_temperature_val;
RTC_DATA_ATTR float last_lux_val;
RTC_DATA_ATTR float last_distance_val;

// State variables
int water_tank_state;
int humid_state;
int temp_state;
int pump_state;
int led_state;
RTC_DATA_ATTR bool active_status = 0;


// Variables for CoT
int soil_avg;
int uv_avg;
int humidity_avg;
int temperature_avg;
int lux_avg;
int distance_avg;

// Long Variables
unsigned long oled_start;
unsigned int compiled_states;
unsigned int new_compiled_states;

Adafruit_AHTX0 aht;                             // Defines the function used to retrive temp and humi
DFRobot_VEML7700 veml;                          // Defines the function used to retrive Lux
CircusESP32Lib circusESP32(server, ssid, psk);  // Defines the function used to communicate to CoT

char wakeup_reason;                             // variabel for external wakeup
void callback(){}                               // callback function for wakeup interupt

void setup(){

  //Start communication
  aht.begin();                    // Starts the function to retreve temp and humid
  veml.begin();                   // Starts the function to retreve Lux value
  
  // pinModes
  pinMode(soilsensor_pin, INPUT);
  pinMode(uvsensor_pin, INPUT);
  pinMode(echo_pin, INPUT);
  pinMode(trigger_pin, OUTPUT);
  pinMode(pump_pin, OUTPUT);
  pinMode(led_pin, OUTPUT);

  // OLED initiation
  tft.init();
  tft.fillScreen(TFT_BLACK);
  tft.setCursor(0, 0, 4);                   // Set "cursor" at top left corner of display (0,0) and select font 4
  tft.setTextColor(TFT_WHITE, TFT_BLACK);  // Set the font colour to be white with a black background
                                          // We can now plot text on screen using the "print" class

  //Setup interrupt on Touch Pad 3 (GPIO15)
  touchAttachInterrupt(T3, callback, Threshold);

  //Configure Touchpad as wakeup source
  wakeup_reason = esp_sleep_get_wakeup_cause();
  
  //Defining wakeup reasons
  esp_sleep_enable_timer_wakeup(sleep_time*second);
  esp_sleep_enable_touchpad_wakeup();

  // Turns on the LED when ESP32 wakes up from sleep if the LED was on inn a previous boot
  if (active_status == 1){
    //ledC Config
    ledcSetup(led_channel, frequency, resolution);
    ledcAttachPin(led_pin, led_channel);
    
    ledcWrite(led_channel, led_brightness);
  }
    
  // Will be true if the ESP is awaken form timer
  if(wakeup_reason == ESP_SLEEP_WAKEUP_TIMER){

    // Populates the value arrays with fresh mesurements
    soil[boot_counter] = get_soil(soilsensor_pin);
    uv[boot_counter] = get_uv(uvsensor_pin);
    distance[boot_counter] = get_waterlevel(trigger_pin,echo_pin);
    lux[boot_counter] = get_lux();
    temperature[boot_counter] = get_temp();
    humidity[boot_counter] = get_humid();

    // Bootcounter update
    boot_counter++;

    // Check if the desired amounts of boots has been reached and then starts to find the average of the values and communicates to CoT
    if (boot_counter == num_readings){
      boot_counter = 0;     //resets the boot counter for new data collection
      
      // Finds average of all the values collected
      soil_avg = find_avg(soil);
      uv_avg = find_avg(uv);
      distance_avg = find_avg(distance);
      lux_avg = find_avg(lux);
      temperature_avg = find_avg(temperature);
      humidity_avg = find_avg(humidity);

      // Remembering the values for OLED
      last_soil_val = soil_avg;
      last_uv_val = uv_avg;
      last_humidity_val = humidity_avg;
      last_temperature_val = temperature_avg;
      last_lux_val = lux_avg;
      last_distance_val = distance_avg;

      // ###### SEND VALUES TO CoT ######
      circusESP32.begin();

      circusESP32.write(soilsensor_key1, soil_avg, token1);
      circusESP32.write(uvsensor_key1, uv_avg, token1);
      circusESP32.write(temperature_key1, temperature_avg, token1);
      circusESP32.write(humidity_key1, humidity_avg, token1);
      circusESP32.write(luxsensor_key1, lux_avg, token1);
      circusESP32.write(ultrasonic_key1, distance_avg, token1);

      // Reads led and pump state
      compiled_states = circusESP32.read(state_array1_key, token1);
      
      // Splitting the integer
      water_tank_state = compiled_states % 10;
      humid_state = (compiled_states / 10) % 10;
      temp_state = (compiled_states / 100) % 10;
      led_state = (compiled_states / 1000) % 10;
      pump_state = (compiled_states / 10000) % 10;

      // Checks if the pump state is anything other than 0 and then initiates watering of the plant  
      if (pump_state != 0){
        //ledC Config
        ledcSetup(pump_channel, frequency, resolution);
        ledcAttachPin(pump_pin, pump_channel);

        pump_state = pump(pump_state, pump_channel);  // Calls on function that finds details of desired watering
        new_compiled_states = compile_states(water_tank_state, humid_state, temp_state, led_state, pump_state, plant);  // Compiling states, making themm ready for sending to CoT
        circusESP32.write(state_array1_key, new_compiled_states, token1);  // Sending the compiled states to CoT to confirm thet the watering of the plant has been executed
      }  

      // Checks if the plant needs light if yes  it initiates lighting of the plant
      if (led_state == 1){
        //ledC Config
        ledcSetup(led_channel, frequency, resolution);
        ledcAttachPin(led_pin, led_channel);
        active_status = 1;  // This variable is to tell the ESP to turn on light at every boot if CoT determines so.
        led_activate(led_channel);  // Function to turn on the LED light
      }
      // Makes sure that the lighting at every boot stops if the plant does not need any more light
      else if (led_state != 1){
        active_status = 0;
      }
    } 
  }
 
  // ###### OLED DISPLAY ######
  if(wakeup_reason == ESP_SLEEP_WAKEUP_TOUCHPAD){

    //Setting the OLED to show the last measured values for 10 seconds after the touch pin is activated
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.println("Verdier");  
    
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.print("Temperatur: ");  
    tft.setTextColor(TFT_GREEN, TFT_BLACK);
    tft.print(int(last_temperature_val));
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.println(" C");

    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.print("Soilsensor: ");  
    tft.setTextColor(TFT_GREEN, TFT_BLACK);
    tft.print(int(last_soil_val));
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.println(" %");

    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.print("Vannmengde: ");  
    tft.setTextColor(TFT_GREEN, TFT_BLACK);
    tft.print(int(last_distance_val));
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.println(" %");

    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.print("Lys: ");  
    tft.setTextColor(TFT_BLUE, TFT_BLACK);
    tft.print(int(last_lux_val));
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.println(" Lux");

    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.print("Fuktighet: ");  
    tft.setTextColor(TFT_BLUE, TFT_BLACK);
    tft.print(int(last_humidity_val));
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.println(" %rH");

    oled_start = millis(); 
    while(oled_start + 10000 > millis()){}    //displaying the values for 10 seconds
  }

  // Makes the ESP go back to sleep
  esp_deep_sleep_start();
}

// Compiles all the values taken as arguments to a array ready to send to CoT
unsigned int compile_states(int water_tank,int humid, int temp, int led, int pump, int plant){
  unsigned int compile = 0;
  compile = water_tank;
  compile += humid * 10;
  compile += temp * 100;
  compile += led * 1000;
  compile += pump * 10000;
  compile += plant * 100000;
  return compile;
}

// Finds the average of the array given as argument 
float find_avg(float array[]){
  float sum  = 0;  // Sets the sum as 0 
  for (int i = 0; i < num_readings; i++){  // Uses a for loop to iterate througt all values in the array
    sum += array[i]; // Adds value to the sum 
  }
  float avg = sum / num_readings;  // Finding average
  return avg;
}

// Finds the percent of soilmoisture in the soil
float get_soil(int pin){
  int value = analogRead(pin);
  float percent = map(value,0,4095,0,100);  // Finding the value in percent
  return percent;
}

// Finds the percent of uv light shining on the plant
float get_uv(int pin){
  int value = analogRead(pin);
  float percent = map(value,0,611,0,100);
  return percent;
}

// Finds the waterlevel in the watermagazine
float get_waterlevel(int trig_pin, int echo_pin){
  unsigned long duration;  
  digitalWrite(trig_pin, LOW);  // Making sure the triggerpin is low
  delayMicroseconds(2);  // Sets a delay of 2 microseconds to make sure that there are no remaining soundwaves in the watermagazine

  digitalWrite(trig_pin, HIGH);  // Makes sound to mesure
  delayMicroseconds(10);  // Sets a delay of 10 microseconds to make sure that there are soundwaves to collect
  digitalWrite(trig_pin, LOW);  // Stops playing sound form triggerpin
  duration = pulseIn(echo_pin, HIGH);  // Mesures the duration it took the sound to travel from the sensor to the water and back
  float distance = duration * 0.0343 / 2;  // Fnds the distance based on the time
  //float distance_percent = map(distance,7,22,0,100);      // 10L bucket not currently in use
  float distance_percent = map(distance,0,8,0,100);         // Candy box currently in use
  distance_percent = 100 - distance_percent;                // Converts the percent for percent empty yo percent full

  return distance_percent;
}

// Finds the amount of light the plant is receaving
float get_lux(){
  float value;
  veml.getAutoALSLux(value);
  return value;
}

// Finds the temperature around the plant
float get_temp(){
  sensors_event_t humidity,temp;
  aht.getEvent(&humidity, &temp);  // populate temp objects with fresh data
  float value = temp.temperature;
  return value;
}

// Finds the room humidity around the plant
float get_humid(){
  sensors_event_t humidity,temp;
  aht.getEvent(&humidity, &temp);  // populate humidity objects with fresh data
  float value = humidity.relative_humidity;
  return value;
}

// Function that controlls the  pumping of water to the plant
int pump(int state, int channel){  // Takes the pump state and the PWM channel the pump is connected to as arguments
  unsigned long duration;
  switch (state){  // Switch case to find out how long the ESP should water the plant
      case 1:
        duration = 1000;
        break;
      
      case 2:
        duration = 2000;
        break;

      case 3:
        duration = 3000;
        break;

      case 4:
        duration = 4000;
        break;

      default:
        duration = 0;
        break;
  }
  state = 0;  // Sets the state to 0 to say that the watering has been executed
  unsigned long start = millis();  // Sets a timestamp to mesure time
  while ((start + duration) > millis()) {  //while loop that is true for a duration
    ledcWrite(channel, pump_magnitude);
  }
  ledcWrite(channel, 0);  // Turns the pump of
  return state;
}

// Function to activete the led when the led state is  collected for CoT
void led_activate(int channel){
  for (int i = 50; i < led_brightness; i++){  // For loop that makes the LED turn on gradualy and not instant
    ledcWrite(channel, i);
    delay(10);
  }
  ledcWrite(channel, led_brightness); // Sets the led to be a predefined brightness
}
 

void loop(){}