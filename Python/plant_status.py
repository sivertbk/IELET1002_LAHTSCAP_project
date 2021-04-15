# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 14:05:49 2021

@author: si_ve
"""

from plant_config import *

# Every plant[i] got its own flag-status register with its values,requirements and statuses.
# Here we update these values




# Get values from soil_sensor and check status
def plant_sensor_status(plant_name, sensor_name):
    if sensor_name == 'soil':
        sensor_name = 'soil_value'
        if plant[plant_name][str(sensor_name)] < plant[plant_name]['water_requirement']:
            status = 'need water'
        else:
            status = 'im good'
    return status

print(plant_sensor_status(0,'soil'))
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
