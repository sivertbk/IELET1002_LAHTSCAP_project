# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 14:05:49 2021

@author: si_ve
"""
from datetime import *
from plant_config import *
import time
import plant_config

# Every plant[i] got its own flag-status register with its values,requirements and statuses.
# Here we update these values


soil_time_tracker = 0
soil_control = False
soil_over_threshold = True

# Get values from soil_sensor and check status
def plant_sensor_status(plant_name, sensor_name):
    if sensor_name == 'soil':
        sensor_name = 'soil_value'
        if plant[str(plant_name)][str(sensor_name)] < plant[plant_name]['water_requirement']:
            status = 'need water'
        else:
            status = 'im good'
    return status

print(plant_sensor_status('0','soil'))




# Get timestamp for soil last_soil_measure
def plant_last_water_timestamp(plant_name, timeformat):
    # This function takes 2 arguments and returns a timestamp for when given plant got water last time
    # Choose plant and what timeformat it should return.
    plant_name = str(plant_name)
    timeformat = str(timeformat)

    if plant_name in plant:
        if statusflag in plant[plant_name]:
            if timeformat == 'epoch':
                timestamp = plant[plant_name][statusflag]
            elif timeformat == 'datetime':
                timestamp = print(datetime.fromtimestamp(
                                    plant[plant_name][statusflag]/1000).strftime('%Y-%m-%d %H:%M:%S'))
            else:
                raise ValueError('ERROR', timeformat, 'is an invalid timeformat. Valid timeformats: epoch, datetime')
        else:
            raise ValueError('ERROR', statusflag, 'is an invalid statusflag. Please use a valid status flag: ',
                    plant[plant_name].keys()) # maybe use for loop for nice print?
    else:
        raise ValueError('ERROR:',plant_name, 'is an invalid plant name. These are the valid plant names:\n',
                plant.keys())
    return timestamp




def plant_soil_check(plant_name):
    current_time = int(time.time())
    soil_value = plant[plant_name]['soil_value']
    Threshold = plant[plant_name]['water_requirement']
    last_water = int(pump_0_key.get()['LastValueTime']/1000)
    water_interval = 10 # 12 Hours interval = 43200 seconds
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


######################################################################################################################

if __name__ == "__main__":
    while True:
        plant_soil_check('0')
        water('0')
        print(datetime.fromtimestamp(plant['0']['last_water']).strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(1)
        if plant['0']['water']:
            plant['0']['water'] = False



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
