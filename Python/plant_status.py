# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 14:05:49 2021

@author: si_ve
"""
from datetime import *
from plant_config import *

# Every plant[i] got its own flag-status register with its values,requirements and statuses.
# Here we update these values




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
def plant_statusflag_timestamp(str(plant_name), str(statusflag), str(timeformat)):
    if plant_name in plant:
        if statusflag in plant:
            timestamp = plant[plant]
            if timeformat == 'epoch':
                timestamp = plant[plant_name][statusflag]
            elif timeformat == 'datetime':

                timestamp = print(datetime.fromtimestamp(
                                    plant[plant_name][statusflag]/1000).strftime('%Y-%m-%d %H:%M:%S'))
            else:
                raise ValueError('ERROR', timeformat, 'is an invalid timeformat. Valid timeformats: epoch, datetime')
        else:
            raise ValueError('ERROR', statusflag, 'is an invalid statusflag. Please use a valid status flag:\n',
                    plant[plant_name].keys()) # maybe use for loop for nice print?
    else:
        raise ValueError('ERROR:',plant_name, 'is an invalid plant name. These are the valid plant names:\n',
                plant.keys())
    return timestamp, print(timestamp)

print(plant_statusflag_timestamp(0,'last_soil_measure', 'datetime'))


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
