# @Date:   2021-05-04T11:07:52+02:00
# @Last modified time: 2021-05-04T12:14:58+02:00



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
    Everytime this is run, it'll return a default plant configuration.
    This function is used whenever a new plant is created and isn't already stored in dictionary with all
    plant's configuration.
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
    Afterwards, it's used to get the values for plants that user has chosen
    and update user configuration panel in Circus of Things.
    (It will also create and store a new configuration into the dictionary if
     there isn't stored any configuration in the dictionary).
    '''

    # From json file, store the dictionary to a variable.
    with open('plant_dictionaries_v2.json') as json_file:
        dictionaries = json.load(json_file)

    # Get the plant number that user has chosen in Circus of Things.
    plant_number = str(CoT.plant_number_key2.get()['Value'])

    # If the plant doesn't exist in dictionary, then create a new key attached with default dictionary needed for a plant. 
    if plant_number not in dictionaries:
        dictionaries[plant_number] = new_default_dictionary()

    # Otherwise, update the user configuration panel with the values that the user want to take a look at.
    else:
        CoT.plant_number_key2.put(dictionaries[plant_number]['plant_number'])
        CoT.active_status_key2.put(dictionaries[plant_number]['active_status'])
        CoT.soil_requirement_key2.put(dictionaries[plant_number]['soil_requirement'])
        CoT.light_requirement_key2.put(dictionaries[plant_number]['lux_requirement'])
        CoT.temperature_maximum_key2.put(dictionaries[plant_number]['temperature_maximum'])
        CoT.temperature_minimum_key2.put(dictionaries[plant_number]['temperature_minimum'])
        CoT.humidity_requirement_key2.put(dictionaries[plant_number]['humidity_requirement'])

    # Then save the dictionary to the json file afterwards
    with open('plant_dictionaries_v2.json', 'w') as json_file:
        json.dump(dictionaries, json_file)

    # Reset the signal new_plant_configuration back to zero, to tell the user that it's finished.
    CoT.new_plant_configuration_key2.put(0)

    return dictionaries # Return the dictionary with every plants configurations.


# plant_number is string, plant_configuration is a single dictionary.
def plant_configuration(plant_number,plant_configuration):
    """
    This function is used for whenever the user wants to change some of the configuration to an already exisiting plant
    """

    # From the json file, get our stored dictionary of every plant configuration user has made .
    with open('plant_dictionaries_v2.json') as json_file:
        dictionaries = json.load(json_file)

    # Update the user configuration for the plant that user has chosen to adjust from Circus of Things.
    plant_configuration['soil_requirement'] = CoT.soil_requirement_key2.get()['Value']
    plant_configuration['lux_requirement'] = CoT.light_requirement_key2.get()['Value']
    plant_configuration['temperature_maximum'] = CoT.temperature_maximum_key2.get()['Value']
    plant_configuration['temperature_minimum'] = CoT.temperature_minimum_key2.get()['Value']
    plant_configuration['humidity_requirement'] = CoT.humidity_requirement_key2.get()['Value']
    plant_configuration['active_status'] = CoT.active_status_key2.get()['Value']

    # Save the new configuration for the chosen plant, and save the whole dictionary to the json file.
    with open('plant_dictionaries_v2.json','w') as json_file:
        dictionaries[plant_number] = plant_configuration
        json.dump(dictionaries, json_file)

    # Reset save_configuration to tell the user that the configuration has been saved.
    CoT.save_configuration_key2.put(0)

    return dictionaries

#### Update plant_dictionary from CoT ####------------------------------------------------------------------------------

def update_plant_sensor_values(plant_dictionary, plant_name):
    """
    Takes sensor values from sensor signal array
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
    Takes sensor values from sensor key list
    This function takes the given plant's dictionary and updates sensor values, then returns updated dictionary.
    Only checks water tank once a day and after pump have been shut off.
    """
    
    current_time = int(time.time()) # Current time in epoch
    now = datetime.now() # Current time in datetime (local)
    last_water = plant_dictionary[str(plant_name)]['last_water']

    plant_dictionary[str(plant_name)]['soil_value'] = CoT.soil_value_key_list[plant_name - 1].get()['Value']
    plant_dictionary[str(plant_name)]['lux_value'] = CoT.lux_value_key_list[plant_name - 1].get()['Value']
    plant_dictionary[str(plant_name)]['temperature_value'] = CoT.temp_value_key_list[plant_name - 1].get()['Value']
    plant_dictionary[str(plant_name)]['humidity_value'] = CoT.humid_value_key_list[plant_name - 1].get()['Value']

    # We request water tank level 5 minutes after pump has been shut off for 5 minutes.
    if ((current_time - last_water) > 300) and ((current_time - last_water) < 600):
        plant_dictionary[str(plant_name)]['water_level'] = CoT.ultrasonic_value_key_list[plant_name - 1].get()['Value']

    # We request water tank level every day between 12:00 and 12:05.
    elif (now.hour == 12) and (now.minute < 6):
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

# Time of control check for soil in seconds. 30 minutes = 1800 seconds
plant_soil_check_control_time = 1800

# Interval time between watering a plant in seconds. 12 Hours interval = 43200 seconds
plant_water_interval = 86400

def check_soil(plant_dictionary, plant_name):
    """
    Function which takes the plant name as an argument and checks if the plant need water or not.
    When the plant need water it changes the plants water status to True(1)
    """

    # Setting up varibales used in function
    current_time = int(time.time()) # current time in epoch
    soil_value = plant_dictionary[str(plant_name)]['soil_value']
    Threshold = plant_dictionary[str(plant_name)]['soil_requirement']
    last_water = plant_dictionary[str(plant_name)]['last_water']
    water_interval = plant_water_interval
    control_wait_time = plant_soil_check_control_time

    # Checking if current soil moisture is under requirement and if it is more than 'water_interval' seconds since last water.
    if (soil_value < Threshold) and ((current_time - last_water) > water_interval):

        # If we are in soil_control we carry on. If not we, set soil_control to True and start the timer.
        if soil_control[str(plant_name)]:

            # If the time now subtracted by the time we entered soil_control is bigger than given control_wait_time we carry on.
            if (current_time - soil_time_tracker[str(plant_name)]) > control_wait_time:
                soil_control[str(plant_name)] = False # soil_control is finished and we set the boolean to False.
                plant_dictionary[str(plant_name)]['pump_state'] = 4 # soil_control has passed and we set pump_state to 1.
                #print('watering plant',str(plant_name)+'!')
                return plant_dictionary

            # We are still waiting for control time to pass. do nothing and return plant_dictionary.
            else:
                return plant_dictionary

        # Set soil_control to True and start the timer. Next time we enter function it will check if the control_wait_time
        # has passed and we can water the plant.
        else:
            print('Plant', str(plant_name), 'soil control in progress! If pass, water in', control_wait_time, 'seconds.')
            soil_time_tracker[str(plant_name)] = int(time.time())
            soil_control[str(plant_name)] = True

    # All is good and we are not going to control the soil value. Set it to False.
    # If we are in soil_control, this will cancel the control.
    else:
        soil_control[str(plant_name)] = False

    return plant_dictionary



#### Lux sensor check ####----------------------------------------------------------------------------------------------

# Lux check variables:

# Dictionary of timestampes for when lux control started for each plant
lux_time_tracker = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0}

# Dictionary of booleans for each plant if lux control is in progress or not
lux_control = {'1':False,'2':False,'3':False,'4':False,'5':False,'6':False,'7':False,'8':False}

# Time for control check for lux in seconds. 5 minutes = 300 seconds
lux_check_control_time = 300

def check_lux(plant_dictionary, plant_name):
    """
    Function which takes the plant name as an argument and checks if the plant need more light or not.
    When the plant need light it changes the plants light status to True(1)
    """
    
    # Setting up variables
    now = datetime.now() # current time in datetime
    current_time = int(time.time()) # current time in epoch
    lux_value = plant_dictionary[str(plant_name)]['lux_value']
    lux_threshold = plant_dictionary[str(plant_name)]['lux_requirement']
    control_wait_time = lux_check_control_time

    # Checks if light value(in lux) is under threshold and time is between 11:00 and 21:00.
    if (lux_value < lux_threshold) and (10 < now.hour) and (now.hour < 21):

        # If we are in lux_control we carry on. If not we, set lux_control to True and start the timer.
        if lux_control[str(plant_name)]:

            # If the time now subtracted by the time we entered lux_control is bigger than given control_wait_time we carry on.
            if (current_time - lux_time_tracker[str(plant_name)]) > control_wait_time:
                plant_dictionary[str(plant_name)]['light_state'] = 1
                lux_control[str(plant_name)] = False
                #print('Light state is set to 1!!!!!!')
                return plant_dictionary

            # We are still waiting for control time to pass. do nothing and return plant_dictionary.
            else:
                return plant_dictionary

        # Set lux_control to True and start the timer. Next time we enter function it will check if the control_wait_time
        # has passed and we can turn on the light.
        else:
            lux_control[str(plant_name)] = True
            lux_time_tracker[str(plant_name)] = int(time.time())
            return plant_dictionary

    # All is good and we are not going to control the light value and we set light_state to False(0).
    # If we are in lux_control, this will cancel the control.
    else:
        plant_dictionary[str(plant_name)]['light_state'] = 0
        lux_control[str(plant_name)] = False
        return plant_dictionary


#### Temperature sensor check ####--------------------------------------------------------------------------------------

"""
A dictionary where time will be stored, if it's control checking up against time, and which stage we are in.
"""

temp_time_tracker = {'1':{'time':time.time(), 'control':False, "stage":0},'2':{'time':time.time(), 'control':False, "stage":0},
                     '3':{'time':time.time(), 'control':False, "stage":0},'4':{'time':time.time(), 'control':False, "stage":0},
                     '5':{'time':time.time(), 'control':False, "stage":0},'6':{'time':time.time(), 'control':False, "stage":0},
                     '7':{'time':time.time(), 'control':False, "stage":0},'8':{'time':time.time(), 'control':False, "stage":0}}

temp_wait_time = 10 # seconds

def check_temperature(plant_dictionary, plant_name):
    """

    Compare sensor values with threshold value, and returns back what state a chosen plant is in.
    """

    # Created and stored everytime function is run
    current_time = time.time()
    
    # Get following values: The value stored in CoT, the thresholds value stored in dictionary from user input
    temp_value = plant_dictionary[str(plant_name)]['temperature_value']
    temp_maximum_threshold = plant_dictionary[str(plant_name)]['temperature_maximum']
    temp_minimum_threshold = plant_dictionary[str(plant_name)]['temperature_minimum']
    
    # Status of control mode & how long it's been in control time. 
    temp_control_time = temp_time_tracker[str(plant_name)]['time']
    temp_control_mode = temp_time_tracker[str(plant_name)]['control']

    # If sensor value is over threshold
    if temp_value > temp_maximum_threshold:
            
        # If the time has passed more than chosen time AND we're in control mode (means we've run it once before).
        if((current_time - temp_control_time > temp_wait_time) and (temp_control_mode == True)):
            
            #Reset control mode
            temp_time_tracker[str(plant_name)]['control'] = False
            
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

        # If first if statement was false, and the system is not in control mode, then start control mode and update time when it started.
        elif temp_time_tracker[str(plant_name)]['control'] == False:
            temp_time_tracker[str(plant_name)]['time'] = time.time()
            temp_time_tracker[str(plant_name)]['control'] = True
        
        # Store the state of temperature regarding current plant environment
        plant_dictionary[str(plant_name)]['temperature_state'] = 2


    # If sensor values are lower than threshold value
    elif temp_value < temp_minimum_threshold:

        # If the time has passed more than chosen time AND we're in control mode (means we've run it once before).
        if((current_time - temp_control_time > temp_wait_time) and (temp_control_mode == True)):
            
            #Reset control mode
            temp_time_tracker[str(plant_name)]['control'] = False
            
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

        # If first if statement was false, and the system is not in control mode, then start control mode and update time when it started.
        elif temp_time_tracker[str(plant_name)]['control'] == False:
            temp_time_tracker[str(plant_name)]['time'] = time.time()
            temp_time_tracker[str(plant_name)]['control'] = True
            
        # Store the state of temperature regarding current plant environment
        plant_dictionary[str(plant_name)]['temperature_state'] = 1


    # Otherwise everythings is okay, and we'll return a state saying so.
    else:
        temp_time_tracker[str(plant_name)]['stage'] = 0
        plant_dictionary[str(plant_name)]['temperature_state'] = 0
    
    
    return plant_dictionary # Return dictionary with updated state that is going to be added to array sent back to ESP through Circus of Things.


#### Relative humidity sensor check ####--------------------------------------------------------------------------------
"""
A dictionary that represent "control mode" for our function. 'control' tells us if the control mode is active or not, 
while 'time' tells us when it's been activated, and 'stage' tells us about how many times a if-statement has been true. 
"""

humid_time_tracker = {'1':{'time':time.time(), 'control':False, "stage":0},'2':{'time':time.time(), 'control':False, "stage":0},
                      '3':{'time':time.time(), 'control':False, "stage":0},'4':{'time':time.time(), 'control':False, "stage":0},
                      '5':{'time':time.time(), 'control':False, "stage":0},'6':{'time':time.time(), 'control':False, "stage":0},
                      '7':{'time':time.time(), 'control':False, "stage":0},'8':{'time':time.time(), 'control':False, "stage":0}}

# How long control mode should be activated, before we change a stage. 
humid_wait_time = 20 #seconds

def check_humidity(plant_dictionary, plant_name):
    """
    Compare sensor values with threshold value, and returns back what state a chosen plant is in.
    """

    # Created and stored  to a variable, whenever function is run
    current_time = time.time()
    
    # Get following values: The humid value stored in CoT and the threshold value stored in dictionary from user input.
    humid_threshold = plant_dictionary[str(plant_name)]['humidity_requirement']
    humid_value = plant_dictionary[str(plant_name)]['humidity_value']
    
    # Status of control mode & how long it's been in control time. 
    humid_control_time = humid_time_tracker[str(plant_name)]['time']
    humid_control_mode = humid_time_tracker[str(plant_name)]['control']
    
    # If humid value is lower than threshold value
    if humid_value < humid_threshold:
        
        # If the time has passed more than chosen time AND we're in control mode (means we've run it once before).
        if((current_time - humid_control_time > humid_wait_time) and (humid_control_mode == True)):
            
        # Reset the control variable, so we can start a new control check for next time.
            humid_time_tracker[str(plant_name)]['control'] = False
            
            # Update the stage variable based on how many times the if-statement has been true.
            if humid_time_tracker[str(plant_name)]['stage'] == 0:
                humid_time_tracker[str(plant_name)]['stage'] = 1

            elif humid_time_tracker[str(plant_name)]['stage'] == 1:
                humid_time_tracker[str(plant_name)]['stage'] = 2

            # After three true statements with no changes, then email owner about it.
            elif humid_time_tracker[str(plant_name)]['stage'] == 2:
                humid_time_tracker[str(plant_name)]['stage'] = 0
                print('email about dryness')
                
        # We would like to run a control mode, checking if system should warn the owner about the state.
        elif humid_time_tracker[str(plant_name)]['control'] == False:
            humid_time_tracker[str(plant_name)]['time'] = time.time()
            humid_time_tracker[str(plant_name)]['control'] = True
            
        # Store the state of humidiity regarding current plant environment
        plant_dictionary[str(plant_name)]['humidity_state'] = 1

    # The humidity is good enough, and we reset stage & store which state humidity is in into dictionary. 
    else:
        humid_time_tracker[str(plant_name)]['stage'] = 0
        plant_dictionary[str(plant_name)]['humidity_state'] = 0
    
    return plant_dictionary # Return the changes that has been made to dictionary. 


#### Ultrasonic sensor/water level check ####---------------------------------------------------------------------------
"""
A dictionary where time will be stored, if it's control checking up against time, and which stage we are in.
"""

def check_water_tank(plant_dictionary, plant_name):
    """
    Checking how much water that are left in the tank.
    """

    # Get the values from ultrasonic sensor for chosen plant
    water_tank_volume = plant_dictionary[str(plant_name)]['water_level']


    # If the water level is between 20 and 10 percent, then return the state representing that
    if (10 < water_tank_volume and water_tank_volume < 20):
        print(f"Warning, water level is at {water_tank_volume}%")
        plant_dictionary[str(plant_name)]['water_level_state'] = 1


    # If it's less than 10 percent, email owner & return the state.
    elif water_tank_volume < 10:
        print("Less than 10% water left. Email owner about it")
        plant_dictionary[str(plant_name)]['water_level_state'] = 2

    # Otherwise the tank has enough water for now.
    else:
        plant_dictionary[str(plant_name)]['water_level_state'] = 0

    return plant_dictionary

#### Pump state & water percentage left in tank (Ultrasonic) ####-------------------------------------------------------

last_system_states = {'1':100000, '2':200000, '3':300000, '4':400000, '5':500000, '6':600000, '7':700000, '8':800000}

def put_system_states_to_CoT(plant_dictionary, plant_name):
    """
    This function reads the states from plant dictionary before it encodes the states and uploads the system states
    to CoT. Also updates last_water if pump_state == 1 and returns it to plant_dictionary.
    """

    # Encode states from plant dictionary into integer with 5 digits
    system_states = CoT.encode_plant_system_states(plant_dictionary, plant_name)

    # If system_states is the same as last_system_states we dont send to CoT.
    if system_states != last_system_states:
        CoT.plant_state_array_list[plant_name - 1].put(system_states) # put states to CoT.
        last_system_states[str(plant_name)] = system_states # update last_system_states to what we sent.

    # Update last watering if pump_state is not 0
    if plant_dictionary[str(plant_name)]['pump_state'] != 0:
        plant_dictionary[str(plant_name)]['last_water'] = int(time.time())

    return plant_dictionary



#### Light state ####---------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    with open("plant_dictionaries_v2.json") as json_file:
        dictionaries = json.load(json_file)

