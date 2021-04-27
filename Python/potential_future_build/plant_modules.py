# @Date:   2021-04-24T13:38:04+02:00
# @Last modified time: 2021-04-27T16:35:03+02:00



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
               'lux_requirement':CoT.light_requirement_key2.get()['Value'],
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
        CoT.light_requirement_key2.put(dictionaries[plant_number]['lux_requirement'])
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
    plant_configuration['lux_requirement'] = CoT.light_requirement_key2.get()['Value']
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



#### Update plant_dictionary from CoT ####------------------------------------------------------------------------------

def update_plant_sensor_values(plant_dictionary, plant_name):
    """
    This function takes the given plant's dictionary and updates sensor values, then returns updated dictionary.
    """
    plant_sensor_dict = CoT.decode_sensor_values(plant_name)
    plant_dictionary[str(plant_name)]['soil_value'] = plant_sensor_dict['soil']
    plant_dictionary[str(plant_name)]['lux_value'] = plant_sensor_dict['lux']
    plant_dictionary[str(plant_name)]['temperature_value'] = plant_sensor_dict['temp']
    plant_dictionary[str(plant_name)]['humidity_value'] = plant_sensor_dict['humid']
    plant_dictionary[str(plant_name)]['water_level'] = plant_sensor_dict['water_level']
    return plant_dictionary

def update_plant_sensor_values_v2(plant_dictionary, plant_name):
    """
    This function takes the given plant's dictionary and updates sensor values, then returns updated dictionary.
    """
    plant_dictionary[str(plant_name)]['soil_value'] = CoT.soil_value_key_list[plant_name - 1].get()['Value']
    plant_dictionary[str(plant_name)]['lux_value'] = CoT.lux_value_key_list[plant_name - 1].get()['Value']
    plant_dictionary[str(plant_name)]['temperature_value'] = CoT.temp_value_key_list[plant_name - 1].get()['Value']
    plant_dictionary[str(plant_name)]['humidity_value'] = CoT.humid_value_key_list[plant_name - 1].get()['Value']
    plant_dictionary[str(plant_name)]['water_level'] = CoT.ultrasonic_value_key_list[plant_name - 1].get()['Value']
    return plant_dictionary


def update_plant_system_states(plant_dictionary, plant_name):
    """
    This function takes the given plant's dictionary and updates system states, then returns updated dictionary.
    """
    plant_state_dict = CoT.decode_plant_system_states(plant_name)
    plant_dictionary[str(plant_name)]['pump_state'] = plant_state_dict['pump_state']
    plant_dictionary[str(plant_name)]['light_state'] = plant_state_dict['light_state']
    plant_dictionary[str(plant_name)]['temperature_state'] = plant_state_dict['temp_state']
    plant_dictionary[str(plant_name)]['humidity_state'] = plant_state_dict['humid_state']
    plant_dictionary[str(plant_name)]['water_level_state'] = plant_state_dict['water_level_state']
    return plant_dictionary


#### Soil moisture check ####-------------------------------------------------------------------------------------------

# Soil check variables:
# Dictionary of timestampes for when soil control started for each plant
soil_time_tracker = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0}
# Dictionary of booleans for each plant if soil control is in progress or not
soil_control = {'1':False,'2':False,'3':False,'4':False,'5':False,'6':False,'7':False,'8':False}
# Dictionary of booleans for each plant if the soil value is over given water requirement
soil_over_threshold = {'1':True,'2':True,'3':True,'4':True,'5':True,'6':True,'7':True,'8':True}
# Time of control check for soil in seconds. 30 minutes = 1800 seconds
plant_soil_check_control_time = 20
# Interval time between watering a plant in seconds. 12 Hours interval = 43200 seconds
plant_water_interval = 5

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
    water_interval = plant_water_interval
    control_wait_time = plant_soil_check_control_time

    if (soil_value < Threshold) and ((current_time - last_water) > water_interval):
        soil_over_threshold[str(plant_name)] = False
        if soil_control[str(plant_name)]:
            if (current_time - soil_time_tracker[str(plant_name)]) > control_wait_time:
                soil_control[str(plant_name)] = False
                soil_time_tracker[str(plant_name)] = 0
                plant_dictionary[str(plant_name)]['pump_state'] = 1
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

#### Pump state & water percentage left in tank (Ultrasonic) ####-------------------------------------------------------

def put_system_states_to_CoT(plant_dictionary, plant_name):
    """
    This function reads the states from plant dictionary before it encodes the states and uploads the system states
    to CoT.
    """
    # encode states from plant dictionary
    system_states = CoT.encode_plant_system_states(plant_dictionary, plant_name)
    # put states to CoT
    CoT.plant_state_array_list[plant_name - 1].put(system_states)
    # update last watering if pump_state is not 0
    if plant_dictionary[str(plant_name)]['pump_state'] != 0:
        plant_dictionary[str(plant_name)]['last_water'] = int(time.time())
    return plant_dictionary


#### Light state ####---------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    print("Oh no")
