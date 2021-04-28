# @Date:   2021-04-24T13:38:04+02:00
# @Last modified time: 2021-04-27T20:16:28+02:00



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
import threading



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

    # Checking if current soil moisture is under requirement and if it is more than 'water_interval' seconds since last water
    if (soil_value < Threshold) and ((current_time - last_water) > water_interval):
        #soil_over_threshold[str(plant_name)] = False # If statement passes,
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
        #soil_over_threshold[str(plant_name)] = True
        return plant_dictionary
    return plant_dictionary



#### Lux sensor check ####----------------------------------------------------------------------------------------------

def lux_check(plant_dictionary, plant_name):
    
    # Setting up variables
    now = datetime.datetime.now()
    lux_value = plant_dictionary[str(plant_name)]['lux_value']
    lux_threshold = plant_dictionary[str(plant_name)]['light_requirement']
    
    
    threading.Timer(300,lux_check).start() # Runs function every 5 minutes. 
    
    # Checks if light value(in lux) is under threshold and in time is between 11:00 and 21:00.
    # If both conditions are true, light state will be set to 1 and activate the light strip.
    if (lux_value < lux_threshold) and (10 < now.hour < 21):
        plant_dictionary[str(plant_name)]['light_state'] = 1
        return plant_dictionary
    else:
        return plant_dictionary
    
        
        
        

#### Temperature sensor check ####--------------------------------------------------------------------------------------

"""
A dictionary where time will be stored, if it's control checking up against time, and which stage we are in.
"""
temp_time_tracker = {'1':{'time':time.time(), 'control':False, "stage":0},'2':{'time':time.time(), 'control':False, "stage":0},
                     '3':{'time':time.time(), 'control':False, "stage":0},'4':{'time':time.time(), 'control':False, "stage":0},
                     '5':{'time':time.time(), 'control':False, "stage":0},'6':{'time':time.time(), 'control':False, "stage":0},
                     '7':{'time':time.time(), 'control':False, "stage":0},'8':{'time':time.time(), 'control':False, "stage":0}}


def checking_temperature(plant_dictionary, plant_name):
    """

    Compare sensor values with threshold value, and returns back what state a chosen plant is in.
    """

    # Created and stored everytime function is run
    current_time = time.time()


    # If the time has passed more than chosen time AND we're in control mode (means we've run it once before) or this is the begininng of the stage, we would like to compare sensor values with threshold values
    ## Delete this row comment ## : As long as sensors always fine, this part will run always. Maybe need a control variable to make sure it doesn't run too often if everythings fine.
    if((current_time - temp_time_tracker[str(plant_name)]['time'] > 10) and (temp_time_tracker[str(plant_name)]['control'] == True)) or (temp_time_tracker[str(plant_name)]['stage'] == 0):

        # Make sure we're reseting control variable, so timer will run again.
        temp_time_tracker[str(plant_name)]['control'] = False

        # Get following values: The value stored in CoT, the thresholds value stored in dictionary from user input.
        temp_value = CoT.temp_value_key_list[plant_name-1].get()['Value']
        temp_maximum_threshold = plant_dictionary[str(plant_name)]['temperature_maximum']
        temp_minimum_threshold = plant_dictionary[str(plant_name)]['temperature_minimum']

        # If sensor value is over threshold
        if temp_value > temp_maximum_threshold:

            # And change the stages of how many times this if statement has been true.
            if temp_time_tracker[str(plant_name)]['stage'] == 0:
                temp_time_tracker[str(plant_name)]['stage'] = 1

            elif temp_time_tracker[str(plant_name)]['stage'] == 1:
                temp_time_tracker[str(plant_name)]['stage'] = 2

            # If it's been true three times, then we want to send an email about it.
            elif temp_time_tracker[str(plant_name)]['stage'] == 2:
                temp_time_tracker[str(plant_name)]['stage'] = 0
                print("email how hot it is")

            # If there's a different stage stored, then change it to 1 as it's "first time" following if statement has been true.
            else:
                temp_time_tracker[str(plant_name)]['stage'] = 1

            plant_dictionary[str(plant_name)]['temperature_state'] = 2

            return plant_dictionary # Return a state value that is going to be added to array sent back to ESP through Circus of Things.

        # If sensor values are lower than threshold value
        elif temp_value < temp_minimum_threshold:

            # Change the stage with how many times this particular if statement has been true
            if temp_time_tracker[str(plant_name)]['stage'] == 0:
                temp_time_tracker[str(plant_name)]['stage'] = 3

            elif temp_time_tracker[str(plant_name)]['stage'] == 3:
                temp_time_tracker[str(plant_name)]['stage'] = 4

            # If it's been true three times in row, we reset the stage, and send an email warning.
            elif temp_time_tracker[str(plant_name)]['stage'] == 4:
                temp_time_tracker[str(plant_name)]['stage'] = 0
                print("email how cold it is")

            # If a different stage is stored, then it's the first time this statement has been true, and we change stage.
            else:
                temp_time_tracker[str(plant_name)]['stage'] = 3

            plant_dictionary[str(plant_name)]['temperature_state'] = 1

            return plant_dictionary # Return a state value that is going to be added to array sent back to ESP through Circus of Things.

        # Otherwise everythings is okay, and we'll return a state saying so.
        else:
            temp_time_tracker[str(plant_name)]['stage'] = 0
            plant_dictionary[str(plant_name)]['temperature_state'] = 0
            return plant_dictionary
        print('return temp state')

    # if first if statement was false, and the system is not in control mode, then start control mode and update time when it started.
    elif temp_time_tracker[str(plant_name)]['control'] == False:
        temp_time_tracker[str(plant_name)]['time'] = time.time()
        temp_time_tracker[str(plant_name)]['control'] = True

        print('start control of temp')

    # If none of the statements are true, then it means the system is currently running in control mode.
    else:
        print(f"waiting for temp for plant {plant_name}")

    return plant_dictionary


#### Relative humidity sensor check ####--------------------------------------------------------------------------------
"""
A dictionary where time will be stored, if it's control checking up against time, and which stage we are in.
"""

humid_time_tracker = {'1':{'time':time.time(), 'control':False, "stage":0},'2':{'time':time.time(), 'control':False, "stage":0},
                      '3':{'time':time.time(), 'control':False, "stage":0},'4':{'time':time.time(), 'control':False, "stage":0},
                      '5':{'time':time.time(), 'control':False, "stage":0},'6':{'time':time.time(), 'control':False, "stage":0},
                      '7':{'time':time.time(), 'control':False, "stage":0},'8':{'time':time.time(), 'control':False, "stage":0}}


def checking_humidity(plant_dictionary, plant_name):
    """
    Compare sensor values with threshold value, and returns back what state a chosen plant is in.
    """

    # Created and stored  to a variable, whenever function is run
    current_time = time.time()

    # If the time has passed more than chosen time AND we're in control mode (means we've run it once before) or this is the begininng of the stage, we would like to compare sensor values with threshold values
    ## Delete this row comment ## : As long as sensors always fine, this part will run always. Maybe need a control variable to make sure it doesn't run too often if everythings fine.
    if((current_time - humid_time_tracker[str(plant_name)]['time'] > 20) and (humid_time_tracker[str(plant_name)]['control'] == True)) or (humid_time_tracker[str(plant_name)]['stage'] == 0):

        # Get following values: The humid value stored in CoT and the threshold value stored in dictionary from user input.
        humid_threshold = plant_dictionary[str(plant_name)]['humidity_requirement']
        humid_value = CoT.humid_value_key_list[plant_name-1].get()['Value']

        # Reset the control variable, so we can start a new control check for next time.
        humid_time_tracker[str(plant_name)]['control'] = False

        # If humid value is lower than threshold value
        if humid_value < humid_threshold:
            print('Air too dry')

            # Update the stage variable based on how many times the if-statement has been true.
            if humid_time_tracker[str(plant_name)]['stage'] == 0:
                humid_time_tracker[str(plant_name)]['stage'] = 1

            elif humid_time_tracker[str(plant_name)]['stage'] == 1:
                humid_time_tracker[str(plant_name)]['stage'] = 2

            # After three true statements with no changes, then email owner about it.
            elif humid_time_tracker[str(plant_name)]['stage'] == 2:
                humid_time_tracker[str(plant_name)]['stage'] = 0
                print('email about dryness')

            plant_dictionary[str(plant_name)]['humidity_state'] = 1
            return plant_dictionary


        # The humidity is good enough
        else:
            print('Its good enough')
            humid_time_tracker[str(plant_name)]['control'] = False
            humid_time_tracker[str(plant_name)]['stage'] = 0
            plant_dictionary[str(plant_name)]['humidity_state'] = 0
            return plant_dictionary


        print('Return humid state')

    # If we've alreadu compared values, then previous statement is false, and we would like to run a control mode, checking if system should warn the owner about the state.
    elif humid_time_tracker[str(plant_name)]['control'] == False:
        humid_time_tracker[str(plant_name)]['time'] = time.time()
        humid_time_tracker[str(plant_name)]['control'] = True
        print('start humid control')

    # System is currently running in a control mode for humidity sensor.
    else:
        print(f"waiting for humid for plant {plant_name}")

    return plant_dictionary


#### Ultrasonic sensor/water level check ####---------------------------------------------------------------------------
"""
A dictionary where time will be stored, if it's control checking up against time, and which stage we are in.
"""
watertank_time_tracker = {'1':{'time':time.time(), 'control':False, "stage":0},'2':{'time':time.time(), 'control':False, "stage":0},
                          '3':{'time':time.time(), 'control':False, "stage":0},'4':{'time':time.time(), 'control':False, "stage":0},
                          '5':{'time':time.time(), 'control':False, "stage":0},'6':{'time':time.time(), 'control':False, "stage":0},
                          '7':{'time':time.time(), 'control':False, "stage":0},'8':{'time':time.time(), 'control':False, "stage":0}}


def checking_water_tank_volume(plant_dictionary, plant_name):
    """
    Checking how much water that are left in the tank.
    """

    # Created and stored  to a variable, whenever function is run
    current_time = time.time()

    # If there has passed an amount of time since last checking the water OR if the pump has recently pumped water, then control how much water is left.
    if((current_time - watertank_time_tracker[str(plant_name)]['time'] > 30) and (watertank_time_tracker[str(plant_name)]['control'] == True)) or (current_time - plant_dictionary[str(plant_name)]['last_water'] < 10):

        # Get the values from ultrasonic sensor for chosen plant
        water_tank_volume = CoT.ultrasonic_value_key_list[plant_name-1].get()['Value']

        # Reset the control mode for this function
        watertank_time_tracker[str(plant_name)]['control'] = False


        # If the water level is between 20 and 10 percent, then return the state representing that
        if (10 < water_tank_volume and water_tank_volume < 20):
            print(f"Warning, water level is at {water_tank_volume}%")
            plant_dictionary[str(plant_name)]['water_level_state'] = 1
            return plant_dictionary


        # If it's less than 10 percent, email owner & return the state.
        elif water_tank_volume < 10:
            print("Email owner about it")
            plant_dictionary[str(plant_name)]['water_level_state'] = 2
            return plant_dictionary


        # Otherwise the tank has enough water for now.
        else:
            print('all fine')
            plant_dictionary[str(plant_name)]['water_level_state'] = 0
            return plant_dictionary


        print('return water tank state')

    # Start control mode if the pump hasn't recently been active or it hasn't been a while since last time sensor been checked.
    elif watertank_time_tracker[str(plant_name)]['control'] == False:
        watertank_time_tracker[str(plant_name)]['time'] = time.time()
        watertank_time_tracker[str(plant_name)]['control'] = True
        print('start watertank control')

    # Function is currently in control mode, checking up on how much time has passed.
    else:
        print(f"waiting for watertank for plant {plant_name}")

    return plant_dictionary

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
