/*
    ##########################  List of needed data to be able to run our code  ##########################
*/

// Libraries
#include <Adafruit_AHTX0.h>    // Library for Temperature/Humidity sensor
#include <CircusESP32Lib.h>    // Library for communication to Circus of Things
#include <DFRobot_VEML7700.h>  // Library for Lux sensor
#include <SPI.h>               // Library for configuration of LCD display
#include <TFT_eSPI.h>          // LCD-hardware-specific library

TFT_eSPI tft = TFT_eSPI();  // Invoke custom library

// Defined values
#define num_readings 12
#define sleep_time 22
#define seconds 1000000         // Converts micro second to second
#define pump_magnitude 255      // An constant that tells how fast the pump should be running when it's activated (given in 8 bits)
#define led_brightness 150
#define Threshold 40            // Higher the value, More sensitive the touchpin will be

// COT Config
char ssid[] = "kameraBad2";     // Name on SSID
char psk[] = "9D2Remember";     // Password for SSID
char token1[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1Nzk0In0.nqXSqXGe2AXcNm4tdMUl7qIzmpAEXwr7UPKf5AtYx4k"; // COT User
char server[] = "www.circusofthings.com"; // Site communication

// Plant (This is important if there are more plants connected to the same RPI)
const int plant = 1;

// COT Signal Keys
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
const int led_pin = 14; // Plant light

// PWM constants
const int pump_channel = 5;
const int led_channel = 6;
// PWM configuration
const int frequency = 5000;
const int resolution = 8;

// RTC_DATA_ATTR used to store data in RTC memory. 
// A counter that tracks how many times ESP32 has been woken up from deep sleep
RTC_DATA_ATTR int boot_counter = 0;

// Array Variables that store sensor measurements
RTC_DATA_ATTR float soil[num_readings];
RTC_DATA_ATTR float uv[num_readings];
RTC_DATA_ATTR float humidity[num_readings];
RTC_DATA_ATTR float temperature[num_readings];
RTC_DATA_ATTR float lux[num_readings];
RTC_DATA_ATTR float waterlevel[num_readings];

// Variables that store last average sensor values (LCD)
RTC_DATA_ATTR int last_soil_val;
RTC_DATA_ATTR int last_uv_val;
RTC_DATA_ATTR int last_humidity_val;
RTC_DATA_ATTR int last_temperature_val;
RTC_DATA_ATTR int last_lux_val;
RTC_DATA_ATTR int last_waterlevel_val;

// State variables
int water_tank_state;
int humid_state;
int temp_state;
int pump_state;
int led_state;
RTC_DATA_ATTR bool led_active_status = 0; 


// Variables that has the average of our measurements, which will then be sent to CoT
int soil_avg;
int uv_avg;
int humidity_avg;
int temperature_avg;
int lux_avg;
int waterlevel_avg;

// Long Variables
unsigned long lcd_start;
unsigned int recent_plant_states;
unsigned int updated_plant_states;

Adafruit_AHTX0 aht;                             // Defines the function used to retrive temp and humi
DFRobot_VEML7700 veml;                          // Defines the function used to retrive Lux
CircusESP32Lib circusESP32(server, ssid, psk);  // Defines the function used to communicate to CoT

char wakeup_reason;                             // variabel for external wakeup
void callback(){}                               // callback function for wakeup interupt


/*
    ##########################    Setup is where the code is being run in    ##########################
*/

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
  
  //Setup interrupt on Touch Pad 3 (GPIO15)
  touchAttachInterrupt(T3, callback, Threshold);

  //Store the reason ESP woke up through a built-in function
  wakeup_reason = esp_sleep_get_wakeup_cause();
  
  //Defining wakeup reasons
  esp_sleep_enable_timer_wakeup(sleep_time*seconds);
  esp_sleep_enable_touchpad_wakeup();

  // If the plant lights was on in the previous boot, then turn it on again. 
  if (led_active_status == 1){
    //ledC Config
    ledcSetup(led_channel, frequency, resolution);
    ledcAttachPin(led_pin, led_channel);
    
    ledcWrite(led_channel, led_brightness);
  }
    
  // Will be true if the ESP was woken up by the timer.
  if(wakeup_reason == ESP_SLEEP_WAKEUP_TIMER){

    // Populates the value arrays with fresh mesurements
    soil[boot_counter] = get_soil(soilsensor_pin);
    uv[boot_counter] = get_uv(uvsensor_pin);
    waterlevel[boot_counter] = get_waterlevel(trigger_pin,echo_pin);
    lux[boot_counter] = get_lux();
    temperature[boot_counter] = get_temp();
    humidity[boot_counter] = get_humid();

    // Bootcounter update
    boot_counter++;

    // Check if the desired amounts of boots has been reached, 
    // then it will find the average value of each sensor array and send it to CoT.
    if (boot_counter == num_readings){
      boot_counter = 0;                     // Resets the boot counter for new data collection
      
      // Finds average of all the values collected
      soil_avg = find_avg(soil);
    //uv_avg = find_avg(uv);
      waterlevel_avg = find_avg(waterlevel);
      lux_avg = find_avg(lux);
      temperature_avg = find_avg(temperature);
      humidity_avg = find_avg(humidity);

      // Remembering the values for LCD
      last_soil_val = soil_avg;
    //last_uv_val = uv_avg;
      last_humidity_val = humidity_avg;
      last_temperature_val = temperature_avg;
      last_lux_val = lux_avg;
      last_waterlevel_val = waterlevel_avg;

      // ###### SEND SENSOR VALUES TO CoT ######
      circusESP32.begin();

      circusESP32.write(soilsensor_key1, soil_avg, token1);
    //circusESP32.write(uvsensor_key1, uv_avg, token1);
      circusESP32.write(temperature_key1, temperature_avg, token1);
      circusESP32.write(humidity_key1, humidity_avg, token1);
      circusESP32.write(luxsensor_key1, lux_avg, token1);
      circusESP32.write(ultrasonic_key1, waterlevel_avg, token1);

      // Reads the system states "array" (regarding the state of the plant) from CoT
      recent_plant_states = circusESP32.read(state_array1_key, token1);
      
      // Splitting up the system state "array" into individual integers. 
      water_tank_state = recent_plant_states % 10;
      humid_state = (recent_plant_states / 10) % 10;
      temp_state = (recent_plant_states / 100) % 10;
      led_state = (recent_plant_states / 1000) % 10;
      pump_state = (recent_plant_states / 10000) % 10;

      // Checks if the pump state is anything other than 0 and then initiates watering of the plant  
      if (pump_state != 0){
        //ledC Config & attach pin to PWM channel
        ledcSetup(pump_channel, frequency, resolution);
        ledcAttachPin(pump_pin, pump_channel);

        // Calls on function that finds details of desired watering
        pump_state = pump(pump_state, pump_channel);  
         
        // Compiling states, making themm ready for sending to CoT                   
        updated_plant_states = encode_states(water_tank_state, humid_state, temp_state, led_state, pump_state, plant); 

        // Sending the updated plant states to CoT to confirm thet the watering of the plant has been executed
        circusESP32.write(state_array1_key, updated_plant_states, token1);  
      }  

      // Checks if the plant needs light, if true, then it will turn on the plant light. 
      if (led_state == 1){
        //ledC Config & attach pin to PWM channel
        ledcSetup(led_channel, frequency, resolution);
        ledcAttachPin(led_pin, led_channel);
        
        led_active_status = 1;          // This variable is to tell the ESP to turn on light at every boot if CoT determines so.
        led_activate(led_channel);  // Function to turn on the LED light
      }
      // Otherwise, turn off the plant light, to make sure it won't be turned on again after each reboot. 
      else if (led_state != 1){
        led_active_status = 0;
      }
    } 
  }
 
  // #############  LCD-DISPLAY  #############
  // If ESP was waken up by touch instead of timer, then print out last taken average measurement. 
  if(wakeup_reason == ESP_SLEEP_WAKEUP_TOUCHPAD){

    // LCD initiation
    tft.init();
    tft.fillScreen(TFT_BLACK);
    tft.setCursor(0, 0, 4);                   // Set "cursor" at top left corner of display (0,0) and select font 4
    tft.setTextColor(TFT_WHITE, TFT_BLACK);   // Set the font colour to be white with a black background
                                            // We can now plot text on screen using the "print" class
                                            
    //Setting the LCD to show the last measured values for 10 seconds after the touch pin is activated
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.println("Verdier");  

    // Shows last average temperature value
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.print("Temperatur: ");  
    tft.setTextColor(TFT_GREEN, TFT_BLACK);
    tft.print(last_temperature_val);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.println(" C");

    // Shows last given average soil moisture value
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.print("Soilsensor: ");  
    tft.setTextColor(TFT_GREEN, TFT_BLACK);
    tft.print(last_soil_val);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.println(" %");

    // Shows how much water is left in the water tank
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.print("Vannmengde: ");  
    tft.setTextColor(TFT_GREEN, TFT_BLACK);
    tft.print(last_waterlevel_val);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.println(" %");

    // Shows the last given average light value
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.print("Lys: ");  
    tft.setTextColor(TFT_BLUE, TFT_BLACK);
    tft.print(last_lux_val);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.println(" Lux");

    // Shows the last given average humidity value. 
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.print("Fuktighet: ");  
    tft.setTextColor(TFT_BLUE, TFT_BLACK);
    tft.print(last_humidity_val);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.println(" %rH");

    lcd_start = millis(); 
    while(lcd_start + 10000 > millis()){}    // Displaying the values for 10 seconds
  }

  // Makes the ESP go back to sleep
  esp_deep_sleep_start();
}

/*
    ##########################    Functions that has been made    ##########################
*/

unsigned int encode_states(int water_tank,int humid, int temp, int led, int pump, int plant){
  /* 
   *  A function that compiles all the values taken as arguments to an array, which will be ready to send to CoT
   */
  unsigned int compile = 0;
  compile = water_tank;
  compile += humid * 10;
  compile += temp * 100;
  compile += led * 1000;
  compile += pump * 10000;
  compile += plant * 100000;
  return compile;
}


float find_avg(float array[]){
  /* 
   * A function that finds the average of the sensor array given as argument 
   */
  float sum  = 0;                          // Sets the sum as 0 
  for (int i = 0; i < num_readings; i++){  // Uses a for loop to iterate througt all values in the array
    sum += array[i];                       // Adds value to the sum 
  }
  float avg = sum / num_readings;          // Finding average
  return avg;
}


float get_soil(int pin){
  /*
   * A function that finds the percent of soilmoisture in the soil
   */
  int value = analogRead(pin);              // Reads the pin value
  float percent = map(value,0,4095,0,100);  // Finding the value in percent
  return percent;
}


float get_uv(int pin){
  /*
   * A function that finds the percent of uv light shining on the plant
   */
  int value = analogRead(pin);
  float percent = map(value,0,611,0,100);
  return percent;
}


float get_waterlevel(int trig_pin, int echo_pin){
  /*
   * A function that finds the waterlevel in the watermagazine
   */
  unsigned long duration;  
  digitalWrite(trig_pin, LOW);   // Making sure the triggerpin is low.
  delayMicroseconds(2);          // Sets a delay of 2 microseconds to make sure that there are no 
                                 // remaining soundwaves in the watermagazine.

  digitalWrite(trig_pin, HIGH);  // Makes sound to measure
  delayMicroseconds(10);         // Sets a delay of 10 microseconds to make sure that there are soundwaves to collect
  digitalWrite(trig_pin, LOW);   // Stops playing sound from triggerpin
  
  duration = pulseIn(echo_pin, HIGH);      // Measures the duration it took for the sound to travel 
                                           // from the sensor to the water and back.
  float distance = (duration * 0.5)/ 29.2; // Finds the distance based on the time
  
  //float distance_percent = map(distance,7,22,0,100);      // 10L bucket not currently in use
  float distance_percent = map(distance,0,8,0,100);         // Candy box currently in use
  distance_percent = 100 - distance_percent;                // Converts the percent for percent empty to percent full

  return distance_percent;
}


float get_lux(){
  /*
   * A function that finds the amount of light the plant is receiving
   */
  float value;                // Define a variable
  veml.getAutoALSLux(value);  // Use a function that will store lux values to variable. 
  return value;
}


float get_temp(){
  /*
   * A function that finds the temperature of plants environment
   */
  sensors_event_t humidity,temp;   // Create an object in memory that will hold the results (sensor values)
  aht.getEvent(&humidity, &temp);  // Populate temp objects with fresh data
  float value = temp.temperature;  // Store the temperature value to a variable
  return value;
}


float get_humid(){
  /*
   * A function that finds the room humidity around the plant
   */
  sensors_event_t humidity,temp;   // Create an object in memory that will hold the results (sensor values)
  aht.getEvent(&humidity, &temp);  // Populate humidity objects with fresh data
  float value = humidity.relative_humidity;
  return value;
}

// Takes the pump state and the PWM channel the pump is connected to as arguments
int pump(int state, int channel){  
  /*
   * Function that controlls how much water should be pumped to the plant
   */
  unsigned long duration;
  switch (state){  // Switch case to find out how long the ESP should water the plant (Duration in ms)
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
  
  state = 0;                                      // Sets the state to 0 to say that the watering has been executed
  unsigned long start = millis();                 // Sets a timestamp to measure time
  unsigned long ending = start + duration;        // Add the duration time to start to get the timestamp when it should end. 
  
  // It'll pump water to plant till current millis() is past ending timestamp. Then it'll stop. 
  while (ending > millis()) { 
    ledcWrite(channel, pump_magnitude);
  }
  
  ledcWrite(channel, 0);                          // Turns off the pump
  return state;
}


void led_activate(int channel){
  /*
   * Function to activate the plant light led when the led state is collected from CoT
   */
  for (int i = 50; i < led_brightness; i++){     // For loop that makes the LED turn on gradually and not instant
    ledcWrite(channel, i);
    delay(10);
  }
  ledcWrite(channel, led_brightness);            // Sets the led to be a predefined brightness
}
 

void loop(){}
