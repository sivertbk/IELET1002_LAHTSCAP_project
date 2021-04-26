'''
This file contains modules & functions related to the plant.
All functions are sorted in the same way it flows through the main loop:
Setup -> config -> update sensors -> soil -> light -> temp -> humid -> water level -> pump state -> light state
'''

from CoT import COT_Signal
from datetime import datetime
import CoT
import time
import json



#### Setup & configuration ####-----------------------------------------------------------------------------------------

def new_default_dictionary():
    """
    A default plant dictionary used for new plant configurations.
    Everytime this is run, the dictionary will get updated values for user controlled variables.
    """
    default = {'plant_number':CoT.plant_number_key2.get()['Value'],
               'active_status':CoT.active_status_key2.get()['Value'],
               'soil_requirement':CoT.soil_requirement_key2.get()['Value'],
               'light_requirement':CoT.light_requirement_key2.get()['Value'],
               'temperature_maximum':CoT.temperature_maximum_key2.get()['Value'],
               'temperature_minimum':CoT.temperature_minimum_key2.get()['Value'],
               'humidity_requirement':CoT.humidity_requirement_key2.get()['Value'],
               'last_water': int(time.time())
               }
    return default


def plant_setup():
    '''
    Used for the first time to get the dictionaries stored in json_file. 
    Afterwards, it's used for whenever the user wants to store a new configuration.
    (And also to see what's already stored)
    '''
    
    with open('plant_dictionaries_v2.json') as json_file:
        dictionaries = json.load(json_file)
    
    plant_number = str(CoT.plant_number_key2.get()['Value'])
    
    if plant_number not in dictionaries:
        dictionaries[plant_number] = new_default_dictionary()
        
    else:
        CoT.plant_number_key2.put(dictionaries[plant_number]['plant_number'])
        CoT.active_status_key2.put(dictionaries[plant_number]['active_status'])
        CoT.soil_requirement_key2.put(dictionaries[plant_number]['soil_requirement'])
        CoT.light_requirement_key2.put(dictionaries[plant_number]['light_requirement'])
        CoT.temperature_maximum_key2.put(dictionaries[plant_number]['temperature_maximum'])
        CoT.temperature_minimum_key2.put(dictionaries[plant_number]['temperature_minimum'])
        CoT.humidity_requirement_key2.put(dictionaries[plant_number]['humidity_requirement'])
    
    with open('plant_dictionaries_v2.json', 'w') as json_file:
        json.dump(dictionaries, json_file)   
        
    CoT.new_plant_configuration_key2.put(0)
    
    return dictionaries


# plant_number is string, plant_configuration is a single dictionary.
def plant_configuration(plant_number,plant_configuration):
    """
    This function is used for whenever the user wants to change some of the configuration to an already exisiting plant
    """
    # Get our stored dictionary of every plant configuration user has made.
    with open('plant_dictionaries_v2.json') as json_file:
        dictionaries = json.load(json_file)

    # Update all values to every key that is based on user input.
    plant_configuration['soil_requirement'] = CoT.soil_requirement_key2.get()['Value']
    plant_configuration['light_requirement'] = CoT.light_requirement_key2.get()['Value']
    plant_configuration['temperature_maximum'] = CoT.temperature_maximum_key2.get()['Value']
    plant_configuration['temperature_minimum'] = CoT.temperature_minimum_key2.get()['Value']
    plant_configuration['humidity_requirement'] = CoT.humidity_requirement_key2.get()['Value']
    plant_configuration['active_status'] = CoT.active_status_key2.get()['Value']

    # Save the updated dictionary to json file.
    with open('plant_dictionaries_v2.json','w') as json_file:
        dictionaries[plant_number] = plant_configuration
        json.dump(dictionaries, json_file)

    # Reset save_configuration
    CoT.save_configuration_key2.put(0)



#### Update sensor values ####------------------------------------------------------------------------------------------

def update_plant_soil_value(plant_dictionary, plant_name):
    """
    This function takes the given plant's soil value from CoT and updates the plant dictionary ['soil_value'].
    """
    # list of all soil keys for each plant, where the index matches all the plant names.
    plant_soil_keys = [CoT.soil_0_key, CoT.soil_1_key, CoT.soil_2_key, CoT.soil_3_key, CoT.soil_4_key, CoT.soil_5_key, CoT.soil_6_key, CoT.soil_7_key]
    plant_dictionary[str(plant_name)]['soil_value'] = plant_soil_keys[int(plant_name)-1].get()['Value']
    return plant_dictionary


def update_plant_water_state(plant_dictionary, plant_name):
    """
    This function takes the given plant's water state from CoT and updates the plant dictionary ['water'].
    """
    plant_pump_keys = [CoT.pump_0_key, CoT.pump_1_key, CoT.pump_2_key, CoT.pump_3_key, CoT.pump_4_key, CoT.pump_5_key, CoT.pump_6_key, CoT.pump_7_key]
    if plant_pump_keys[int(plant_name)-1].get()['Value'] == 1:
        plant_dictionary[str(plant_name)]['water'] = True
    elif plant_pump_keys[int(plant_name)-1].get()['Value'] == 0:
        plant_dictionary[str(plant_name)]['water'] = False
    return plant_dictionary




#### Soil moisture check ####-------------------------------------------------------------------------------------------

# Soil check variables:
# Dictionary of timestampes for when soil control started for each plant
soil_time_tracker = {'0':[],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[]}
# Dictionary of booleans for each plant if soil control is in progress or not
soil_control = {'0':False,'1':False,'2':False,'3':False,'4':False,'5':False,'6':False,'7':False}
# Dictionary of booleans for each plant if the soil value is over given water requirement
soil_over_threshold = {'0':True,'1':True,'2':True,'3':True,'4':True,'5':True,'6':True,'7':True}

def plant_soil_check(plant_dictionary, plant_name):
    """
    Function which takes the plant name as an argument and checks if the plant need water or not.
    When the plant need water it changes the plants water status to True
    """
    if 'last_water' not in plant_dictionary[str(plant_name)].keys(): # Adding 'last_water' if not allready in dictionary
        plant_dictionary[str(plant_name)]['last_water'] = []

    # setting up varibales used in function
    current_time = int(time.time()) # current time in epoch
    soil_value = plant_dictionary[str(plant_name)]['soil_value']
    Threshold = plant_dictionary[str(plant_name)]['soil_requirement']
    last_water = plant_dictionary[str(plant_name)]['last_water']
    water_interval = 5 # 12 Hours interval = 43200 seconds(25 seconds offset/lag)
    control_wait_time = 10 # control wait time 30 minutes = 1800 seconds
    #global soil_control, soil_time_tracker

    if (soil_value < Threshold) and ((current_time - last_water) > water_interval):
        soil_over_threshold[str(plant_name)] = False
        if soil_control[str(plant_name)]:
            if (current_time - soil_time_tracker[str(plant_name)]) > control_wait_time:
                soil_control[str(plant_name)] = False
                soil_time_tracker[str(plant_name)] = 0
                plant_dictionary[str(plant_name)]['water'] = True
                print('watering plant',str(plant_name)+'!')
                return plant_dictionary
            else:
                return plant_dictionary
        else:
            print('Plant', str(plant_name), 'soil control in progress! If pass, water in', control_wait_time, 'seconds.')
            soil_time_tracker[str(plant_name)] = int(time.time())
            soil_control[str(plant_name)] = True

    else:
        soil_control[str(plant_name)] = False
        soil_over_threshold[str(plant_name)] = True
        return plant_dictionary
    return plant_dictionary



#### Lux sensor check ####----------------------------------------------------------------------------------------------



#### Temperature sensor check ####--------------------------------------------------------------------------------------
def checking_temperature(plant_dictionary, plant_name):
    
    temp_sensor_keys = [CoT.temp_0_key, CoT.temp_1_key, CoT.temp_2_key, CoT.temp_3_key,
                        CoT.temp_4_key, CoT.temp_5_key, CoT.temp_6_key, CoT.temp_7_key]
    
    temp_value = temp_sensor_keys[plant_name-1].get()['Value']
    temp_maximum_threshold = plant_dictionary[plant_name]['temperature_maximum']
    temp_minimum_threshold = plant_dictionary[plant_name]['temperature_minimum']
    
    if temp_value > temp_maximum_threshold:
        print("Hot hot hot hot")
    elif temp_value < temp_minimum_threshold:
        print("Why so cold?")
    else:
        print("Paradise")

#### Relative humidity sensor check ####--------------------------------------------------------------------------------
def checking_humidity(plant_dictionary, plant_name):
    
    humid_sensor_keys = [CoT.humid_0_key, CoT.humid_1_key, CoT.humid_2_key, CoT.humid_3_key,
                         CoT.humid_4_key, CoT.humid_5_key, CoT.humid_6_key, CoT.humid_7_key]
    
    humid_value = humid_sensor_keys[plant_name-1].get()['Value']
    humid_threshold = plant_dictionary[plant_name]['humidity_requirement']
    
    if humid_value < humid_threshold:
        print("Too dry?")
    else:
        print("Possibility for having too much humidity")


#### Ultrasonic sensor/water level check ####---------------------------------------------------------------------------
def checking_water_tank_volume(plant_dictionary, plant_name):
    
    ultrasonic_sensor_keys = [CoT.ultrasonic_0_key, CoT.ultrasonic_1_key, CoT.ultrasonic_2_key, CoT.ultrasonic_3_key,
                              CoT.ultrasonic_4_key, CoT.ultrasonic_5_key, CoT.ultrasonic_6_key, CoT.ultrasonic_7_key]
    
    water_tank_volume = ultrasonic_sensor_keys[plant_name-1].get()['Value']
    
    if (10 < water_tank_volume and water_tank_volume < 20):
        print(f"Warning, water level is at {water_tank_volume}%")
        
    elif water_tank_volume < 10:
        print("Oh no")
        
    else:
        print('all fine')

#### Pump state & water percentage left in tank (Ultrasonic) ####----------------------------------------------------------------------------------------------------

def water(plant_dictionary, plant_name):
    """
    This function reads the bool for every plants water state and sends a signal to CoT if its time for a shower.
    When water state == True it updates last watering.
    """
    plant_pump_keys = [CoT.pump_0_key, CoT.pump_1_key, CoT.pump_2_key, CoT.pump_3_key, CoT.pump_4_key, CoT.pump_5_key, CoT.pump_6_key, CoT.pump_7_key]
    if plant_dictionary[str(plant_name)]['water']:
        plant_dictionary[str(plant_name)]['last_water'] = int(time.time())
        plant_pump_keys[int(plant_name)-1].put(1)
        return 
    else:
        return


#### Light state ####---------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    print("Oh no")
