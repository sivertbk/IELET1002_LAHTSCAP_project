# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 14:05:49 2021

@author: si_ve
"""
from datetime import *
from plant_config import *
import time
from CoT import *

# Every plant[i] got its own flag-status register with its values,requirements and statuses.
# Here we update these values


soil_time_tracker = 0
soil_control = False
soil_over_threshold = True



# Get timestamp for soil last_soil_measure
def plant_last_water_timestamp(plant_name, timeformat):
    """This function takes 2 arguments and returns a timestamp for when given plant got water last time.
    Choose plant and what timeformat it should return your value as."""
    # list of all pump keys for each plant, where the index matches all the plant names.
    plant_pump_keys = [pump_0_key, pump_1_key, pump_3_key, pump_4_key, pump_5_key, pump_6_key, pump_7_key]

    # Calls the last time pump state changed in CoT and stores the value in 'timestamp'.
    if timeformat == ('epoch' or 'unix time'):
        timestamp = plant_pump_keys[int(plant_name)].get()['LastValueTime']/1000

    elif timeformat == 'datetime':
        timestamp = datetime.fromtimestamp(plant_pump_keys[int(plant_name)].get()['LastValueTime']/1000).strftime('%Y-%m-%d %H:%M:%S')

    return timestamp




def plant_soil_check(plant_name):
    """Function which takes the plant name as an argument and checks if the plant need water or not.
    When the plant need water it changes the plants water status to True"""
    current_time = int(time.time()) # current time in epoch
    soil_value = plant[plant_name]['soil_value'] # ISSUE: values dont update???
    Threshold = plant[plant_name]['water_requirement']
    last_water = plant_last_water_timestamp(plant_name,'epoch')
    water_interval = 1 - 25 # 12 Hours interval = 43200 seconds(25 seconds offset/lag)
    wait_time = 5 # control wait time 30 minutes = 1800 seconds
    global soil_control, soil_time_tracker

    if (soil_value < Threshold) and ((current_time - last_water) > water_interval):
        soil_over_threshold = False
        if soil_control:
            if (current_time - soil_time_tracker) > wait_time:
                soil_control = False
                soil_time_tracker = 0
                plant[plant_name]['water'] = True
                return print('watering!')
            else:
                return
        else:
            print('Soil control in progress... hold on')
            soil_time_tracker = int(time.time())
            soil_control = True

    else:
        soil_over_threshold = True
        soil_time_tracker = time.time()
        return print('soil is good enough :D')
    return

def water(plant_name):
    if plant[plant_name]['water']:
        return pump_0_key.put(1)
    else:
        return

def plant_sensorvalue_control(plant_name, sensor, wait_time):
    # This function takes 3 arguments and returns a boolean
    return bool

while True:
    plant_soil_check('0')
    water('0')
    print(datetime.fromtimestamp(plant_last_water_timestamp('0','epoch')).strftime('%Y-%m-%d %H:%M:%S'))
    time.sleep(1)
    if plant['0']['water']:
        plant['0']['water'] = False
    print(plant['0']['soil_value'])
######################################################################################################################

if __name__ == "__main__":
    #print(plant_last_water_timestamp('0','epoch'))
    """while True:
        plant_soil_check('0')
        water('0')
        print(datetime.fromtimestamp(plant_last_water_timestamp('0','epoch')).strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(1)
        if plant['0']['water']:
            plant['0']['water'] = False
        print(plant['0']['soil_value'])"""



    # CoT get values
        # Get value from CoT too soil_sensor_value(plant)
        # update time and value for last_soil_measure{time:datetime, soil:value}


    # Value should be under SOIL_THRESHOLD and LAST_WATER_THRESHOLD before watering initiates.

        # if both passes, eneable watering flag



# water the plant?

    # YES:
        # what plant?
        # how much water does that plant need?
        # update last_water[plant]
        # reset watering flag

    # NO:
        # aight. bye.
