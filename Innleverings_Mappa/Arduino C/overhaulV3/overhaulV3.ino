
// Library
#include <Adafruit_AHTX0.h>
#include <CircusESP32Lib.h>
#include <DFRobot_VEML7700.h>
#include <SPI.h>            // library for configuration of OLED display
#include <TFT_eSPI.h>       // Hardware-specific library

TFT_eSPI tft = TFT_eSPI();  // Invoke custom library


// Download links til lib brukt:
//    https://github.com/DFRobot/DFRobot_VEML7700
//    https://github.com/adafruit/Adafruit_AHTX0
//    https://circusofthings.com
//    lib mappe i giten

#define num_readings 6
#define sleep_time 7
#define second 1000000         // converts micro seconds to seconds
#define pump_magnitude 255     // Constant to say how fast the pump should run when it is running (given in 8 bits)
#define led_brightness 150
#define Threshold 40 /* Greater the value, more the sensitivity on touchpin*/

// COT Config
char ssid[] = "kameraBad2"; // Name on SSID
char psk[] = "9D2Remember"; // Password for SSID
char token1[] = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1Nzk0In0.nqXSqXGe2AXcNm4tdMUl7qIzmpAEXwr7UPKf5AtYx4k"; // COT User
char server[] = "www.circusofthings.com"; // Site communication

// Plant (Important if more plants are connected to the same RPi)
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

// PWM Config
const int pump_channel = 5;
const int led_channel = 6;

const int frequency = 5000;
const int resolution = 8;


// Counter to track how many times ESP32 has akaken form its deep sleep
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

RTC_DATA_ATTR char text_color_temp;
RTC_DATA_ATTR char text_color_soil;
RTC_DATA_ATTR char text_color_water;

// State variables
int water_tank_state;
int humid_state;
int temp_state;
int pump_state;
int led_state;

unsigned int compiled_states;
unsigned int new_compiled_states;

// Variables for CoT
int soil_avg;
int uv_avg;
int humidity_avg;
int temperature_avg;
int lux_avg;
int distance_avg;

// Long Variables
//unsigned long duration;
//unsigned long time;
//unsigned long pump_duration;      // Given in ms and determines how long the pump should run
//unsigned long pump_start = 0;
//unsigned long wait_start = 0;
//unsigned long wait_duration = 5000;
unsigned long oled_start;

// Pump Logic Variables
//bool pump_active = 0;             // Bool variable that determines if the pump is active or not
//int pump_strenght = 0;            // Variable to determine how fast the pump should run
//const int pump_magnitude = 255;   // Constant to say how fast the pump should run when it is running (given in 8 bits)


Adafruit_AHTX0 aht;                             // Defines the function used to retrive temp and humi
DFRobot_VEML7700 veml;                          // Defines the function used to retrive Lux
CircusESP32Lib circusESP32(server, ssid, psk);  // Defines the function used to communicate to CoT

char wakeup_reason; // variable for eksternal wakeup
void callback(){} //callback function for touch interrupt

void setup(){

  //Start communication
  Serial.begin(115200);
  aht.begin();                    // Starts the function to retreve temp and humid
  veml.begin();                   // Starts the function to retreve Lux value
  circusESP32.begin();
  
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
  tft.setCursor(0, 0, 4);  // Set "cursor" at top left corner of display (0,0) and select font 4
  tft.setTextColor(TFT_WHITE, TFT_BLACK);  // Set the font colour to be white with a black background
  // We can now plot text on screen using the "print" class

  //ledC Config
  ledcSetup(pump_channel, frequency, resolution);
  ledcAttachPin(pump_pin, pump_channel);
  
  ledcSetup(led_channel, frequency, resolution);
  ledcAttachPin(led_pin, led_channel);

  //Setup interrupt on Touch Pad 3 (GPIO15)
  touchAttachInterrupt(T3, callback, Threshold);

  //Configure Touchpad as wakeup source
  wakeup_reason = esp_sleep_get_wakeup_cause();
  //Defining wakeup reasons
  esp_sleep_enable_timer_wakeup(sleep_time*second);
  esp_sleep_enable_touchpad_wakeup();

  // Code for mesurement when awakening for sleep
  if(wakeup_reason == ESP_SLEEP_WAKEUP_TIMER){
    
    Serial.println("Collecting values: " + String(boot_counter) + ". for: " + String(num_readings) + ". times");
    // retreaving data
    soil[boot_counter] = get_soil(soilsensor_pin);
    uv[boot_counter] = get_uv(uvsensor_pin);
    distance[boot_counter] = get_waterlevel(trigger_pin,echo_pin);
    lux[boot_counter] = get_lux();
    temperature[boot_counter] = get_temp();
    humidity[boot_counter] = get_humid();

    //bootcounter update
    boot_counter++;

    //check if bootcounter == numreadings
    if (boot_counter == num_readings){
      Serial.println("Finding average");
      //get average
      //boot_counter = 0;
      
      soil_avg = find_avg(soil);
      uv_avg = find_avg(uv);
      distance_avg = find_avg(distance);
      lux_avg = find_avg(lux);
      temperature_avg = find_avg(temperature);
      humidity_avg = find_avg(humidity);

      //test
      soil_avg = 15;
      uv_avg = 15;
      distance_avg = 15;
      lux_avg = 15;
      temperature_avg = 15;
      humidity_avg = 15;

      // Remembering the values for OLED
      last_soil_val = soil_avg;
      last_uv_val = uv_avg;
      last_humidity_val = humidity_avg;
      last_temperature_val = temperature_avg;
      last_lux_val = lux_avg;
      last_distance_val = distance_avg;
      
      // ###### SEND VERDIER TIL CoT ######
      circusESP32.write(soilsensor_key1, soil_avg, token1);
      circusESP32.write(uvsensor_key1, uv_avg, token1);
      circusESP32.write(temperature_key1, temperature_avg, token1);
      circusESP32.write(humidity_key1, humidity_avg, token1);
      circusESP32.write(luxsensor_key1, lux_avg, token1);
      circusESP32.write(ultrasonic_key1, distance_avg, token1);
    } 
  }
  if (wakeup_reason == ESP_SLEEP_WAKEUP_TOUCHPAD || boot_counter == num_readings){
    boot_counter = 0;     //resetter bootcounter for ny datasamlingsyklus
    Serial.print("                    skjekker input array for endringer");
    //leser led status og pumpe status
    compiled_states = circusESP32.read(state_array1_key, token1);
    
    // splitting the integer
    water_tank_state = compiled_states % 10;
    humid_state = (compiled_states / 10) % 10;
    temp_state = (compiled_states / 100) % 10;
    led_state = (compiled_states / 1000) % 10;
    pump_state = (compiled_states / 10000) % 10;

    Serial.println(String(compiled_states) + "Led state: " +String(led_state) + "Pump state: " +String(pump_state));
    if (pump_state != 0){
      pump(pump_state, pump_channel);
      pump_state = 0;
      new_compiled_states = compile_states(water_tank_state, humid_state, temp_state, led_state, pump_state, plant);
      circusESP32.write(state_array1_key, new_compiled_states, token1);
    }  
    if (led_state != 0){
      //skru på led stripe
      led_activate(led_state, led_channel);
    }
  }


  // ###### OLED DISPLAY ######
  // the pinns for the OLED display are defined in the user.setup file in the espi library
  // ground -> GRN, VCC -> 3V3, SCL -> 18, SDA -> 23, RES -> 4, DC -> 2
  else if(wakeup_reason == ESP_SLEEP_WAKEUP_TOUCHPAD){
    //leser led status og pumpe status
    compiled_states = circusESP32.read(state_array1_key, token1);
    
    // splitting the integer
    water_tank_state = compiled_states % 10;
    humid_state = (compiled_states / 10) % 10;
    temp_state = (compiled_states / 100) % 10;

    oled_start = millis();
    //if statements to determine the color of the displayed values based on how "good" they are
    if(temp_state = 0){
      text_color_temp = TFT_GREEN;
    }
    else if(temp_state = 1){
      text_color_temp = TFT_BLUE;
    }
    else if(temp_state = 2){
      text_color_temp = TFT_RED;
    }

    if(last_soil_val < 25){
      text_color_soil = TFT_BLUE;
    }
    else if(last_soil_val > 25 && last_soil_val < 75){
      text_color_soil = TFT_GREEN;
    }
    else if(last_soil_val > 75){
      text_color_soil = TFT_RED;
    }

    if(water_tank_state == 0){
    text_color_water = TFT_GREEN;
    }
    else if (water_tank_state == 1){
      text_color_water = TFT_BLUE;
    }
    else if (water_tank_state == 2){
      text_color_water = TFT_RED;
    }

    //Setting the OLED to show the last measured values for 10 seconds after the touch pin is activated
      tft.setTextColor(TFT_WHITE, TFT_BLACK);
      tft.print("Temperatur:");  
      tft.setTextColor(text_color_temp, TFT_BLACK);
      tft.print(int(last_temperature_val));
      tft.setTextColor(TFT_WHITE, TFT_BLACK);
      tft.println("C");

      tft.setTextColor(TFT_WHITE, TFT_BLACK);
      tft.print("Soilsensor:");  
      tft.setTextColor(text_color_soil, TFT_BLACK);
      tft.print(int(last_soil_val));
      tft.setTextColor(TFT_WHITE, TFT_BLACK);
      tft.println("%");

      tft.setTextColor(TFT_WHITE, TFT_BLACK);
      tft.print("Vannmengde:");  
      tft.setTextColor(text_color_water, TFT_BLACK);
      tft.print(int(last_distance_val));
      tft.setTextColor(TFT_WHITE, TFT_BLACK);
      tft.println("%");
    while(oled_start + 10000 > millis()){}//displaying the values for 10 seconds

    Serial.println("                                                       Det funker");
  }

//go back to sleep
  esp_deep_sleep_start();
}


unsigned int compile_states(int water_tank,int humid, int temp, int led, int pump, int plant){
  unsigned int compile = 0;
  compile = water_tank;
  compile = compile + humid * 10;
  compile = compile + temp * 100;
  compile = compile + led * 1000;
  compile = compile + pump * 10000;
  compile = compile + plant * 100000;
  return compile;
}

float find_avg(float array[]){
  float sum  = 0;
  for (int i = 0;i < num_readings; i++){
    //Serial.println(String(i) + ", " + String(array[i]));
    sum = sum + array[i];
  }
  float avg = sum / num_readings;
  return avg;
}

float get_soil(int pin){
  int value = analogRead(pin);
  float percent = map(value,0,4095,0,100);// finner den prosentvise verdien for jordfuktighet
  //Serial.println(); Serial.print("                Soil Sensor in %: "); Serial.println(value);
  return percent;
}

float get_uv(int pin){
  int value = analogRead(pin);                    // denne viser for detmeste 0 men om den får direkte sollys gir den verdier (16.04 kl 14ish ga den 400 ved direkte sollys)
  float percent = map(value,0,611,0,100);     // usikker på nevner verdien, kan være høyere // hyeste målt verdi 1300 20.04 611
  //Serial.print("                UV in %: "); Serial.println(value);
  return percent;
}

float get_waterlevel(int trig_pin, int echo_pin){    //Ultrasonisk sensor
  unsigned long duration;
  digitalWrite(trig_pin, LOW);
  delayMicroseconds(2);

  digitalWrite(trig_pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig_pin, LOW);
  duration = pulseIn(echo_pin, HIGH);
  float distance = duration * 0.034 / 2;
  //Serial.print("                Distance: "); Serial.print(distance); Serial.println(" cm");
  float distance_percent = map(distance,7,22,0,100);

  return distance_percent;
}

float get_lux(){
  float value;
 
  veml.getALSLux(value);
  Serial.print("                Lux:"); Serial.print(value); Serial.println(" lx");
  return value;
  // har fått lux = 274,000lx (ish) med lys av mobil
}

float get_temp(){
  sensors_event_t humidity,temp;
  aht.getEvent(&humidity, &temp);// populate temp objects with fresh data
  Serial.print("                Temperature: "); Serial.print(temp.temperature); Serial.println(" degrees C");
  float value = temp.temperature;
  return value;
}

float get_humid(){
  sensors_event_t humidity,temp;
  aht.getEvent(&humidity, &temp);// populate humidity objects with fresh data
  Serial.print("                Humidity: "); Serial.print(humidity.relative_humidity); Serial.println("% rH");

  float value = humidity.relative_humidity;
  return value;
}

void pump(int state, int channel){
  unsigned long duration;
  switch (state){
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
  //Serial.println("                                  HEI HAA");
  state = 0;
  unsigned long start = millis();
  while ((start + duration) > millis()) {
    ledcWrite(channel, pump_magnitude);
  }
  ledcWrite(channel, 0);
}

void led_activate(int state, int channel){
  Serial.println("led funksjon aktivert");
  if (state == 1){
    for (int i = 50; i < led_brightness; i++){
      ledcWrite(channel, i);
      delay(10);
    }
    ledcWrite(channel, led_brightness);
  }
  else{
    ledcWrite(channel, 0);
  }
  Serial.println("led_state: " + String(state));
}
 
void loop(){}
