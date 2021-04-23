# @Date:   2021-04-21T14:03:41+02:00
# @Last modified time: 2021-04-23T12:50:41+02:00



'''
This file contains modules & functions related to the plant.
All functions are sorted in the same way it flows through the main loop:
Setup -> config -> update sensors -> soil -> light -> temp -> humid -> water level -> pump state -> light state
'''

from CoT import COT_Signal
from datetime import *
from CoT import *
import time
import json



#### Setup & configuration ####-----------------------------------------------------------------------------------------

def new_default_dictionary():
    """
    A default plant dictionary used for new plant configurations.
    Everytime this is run, the dictionary will get updated values for user controlled variables.
    """
    default = {'plant_number':plant_number_key2.get()['Value'],
               'active_status':active_status_key2.get()['Value'],
               'soil_requirement':soil_requirement_key2.get()['Value'],
               'light_requirement':light_requirement_key2.get()['Value'],
               'temperature_maximum':temperature_maximum_key2.get()['Value'],
               'temperature_minimum':temperature_minimum_key2.get()['Value'],
               'humidity_requirement':humidity_requirement_key2.get()['Value'],
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
    
    plant_number = str(plant_number_key2.get()['Value'])
    
    if plant_number not in dictionaries:
        dictionaries[plant_number] = new_default_dictionary()
        
    else:
        plant_number_key2.put(dictionaries[plant_number]['plant_number'])
        active_status_key2.put(dictionaries[plant_number]['active_status'])
        soil_requirement_key2.put(dictionaries[plant_number]['soil_requirement'])
        light_requirement_key2.put(dictionaries[plant_number]['light_requirement'])
        temperature_maximum_key2.put(dictionaries[plant_number]['temperature_maximum'])
        temperature_minimum_key2.put(dictionaries[plant_number]['temperature_minimum'])
        humidity_requirement_key2.put(dictionaries[plant_number]['humidity_requirement'])
    
    with open('plant_dictionaries_v2.json', 'w') as json_file:
        json.dump(dictionaries, json_file)   
        
    new_plant_configuration_key2.put(0)
    
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
    plant_configuration['soil_requirement'] = soil_requirement_key2.get()['Value']
    plant_configuration['light_requirement'] = light_requirement_key2.get()['Value']
    plant_configuration['temperature_maximum'] = temperature_maximum_key2.get()['Value']
    plant_configuration['temperature_minimum'] = temperature_minimum_key2.get()['Value']
    plant_configuration['humidity_requirement'] = humidity_requirement_key2.get()['Value']
    plant_configuration['active_status'] = active_status_key2.get()['Value']

    # Save the updated dictionary to json file.
    with open('plant_dictionaries_v2.json','w') as json_file:
        dictionaries[plant_number] = plant_configuration
        json.dump(dictionaries, json_file)

    # Reset save_configuration
    save_configuration_key2.put(0)










#### Update sensor values ####------------------------------------------------------------------------------------------

def plant_last_water_timestamp(plant_name, timeformat):
    """
    This function takes 2 arguments and returns a timestamp for when given plant got water last time.
    Choose plant and what timeformat it should return your value as.
    """
    # list of all pump keys for each plant, where the index matches all the plant names.
    plant_pump_keys = [pump_0_key, pump_1_key, pump_3_key, pump_4_key, pump_5_key, pump_6_key, pump_7_key]

    # Calls the last time pump state changed in CoT and stores the value in 'timestamp'.
    if timeformat == ('epoch' or 'unix time'):
        timestamp = plant_pump_keys[int(plant_name)-1].get()['LastValueTime']/1000
    elif timeformat == 'datetime':
        timestamp = datetime.fromtimestamp(plant_pump_keys[int(plant_name)-1].get()['LastValueTime']/1000).strftime('%Y-%m-%d %H:%M:%S')
    return timestamp


def update_plant_soil_value(plant_dictionary, plant_name):
    """
    This function takes the given plant's soil value from CoT and updates the plant dictionary ['soil_value'].
    """
    # list of all soil keys for each plant, where the index matches all the plant names.
    plant_soil_keys = [soil_0_key, soil_1_key, soil_2_key, soil_3_key, soil_4_key, soil_5_key, soil_6_key, soil_7_key]
    plant_dictionary[str(plant_name)]['soil_value'] = plant_soil_keys[int(plant_name)-1].get()['Value']
    return plant_dictionary


def update_plant_water_state(plant_dictionary, plant_name):
    """
    This function takes the given plant's water state from CoT and updates the plant dictionary ['water'].
    """
    plant_pump_keys = [pump_0_key, pump_1_key, pump_3_key, pump_4_key, pump_5_key, pump_6_key, pump_7_key]
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



#### Relative humidity sensor check ####--------------------------------------------------------------------------------



#### Ultrasonic sensor/water level check ####---------------------------------------------------------------------------



#### Pump state ####----------------------------------------------------------------------------------------------------

def water(plant_dictionary, plant_name):
    """
    This function reads the bool for every plants water state and sends a signal to CoT if its time for a shower.
    When water state == True it updates last watering.
    """
    plant_pump_keys = [pump_0_key, pump_1_key, pump_2_key, pump_3_key, pump_4_key, pump_5_key, pump_6_key, pump_7_key]
    if plant_dictionary[str(plant_name)]['water']:
        plant_dictionary[str(plant_name)]['last_water'] = int(time.time())
        plant_pump_keys[int(plant_name)-1].put(1)
        return 
    else:
        return


#### Light state ####---------------------------------------------------------------------------------------------------















if __name__ == "__main__":
    print("Oh no")
