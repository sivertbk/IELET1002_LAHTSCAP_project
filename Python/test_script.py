# @Author: Sivert Berg Knudsen <sivertbk>
# @Date:   2021-04-15T17:02:18+02:00
# @Email:  si_vert@hotmail.com
# @Filename: testing.py
# @Last modified by:
# @Last modified time: 2021-04-20T21:05:00+02:00
from CoT import *

def update_plant_soil_value(plant_name):
    """
    This function takes the given plant's soil value from CoT and updates the plant dictionary ['soil_value'].
    """
    # list of all soil keys for each plant, where the index matches all the plant names.
    plant_soil_keys = [soil_0_key, soil_1_key, soil_2_key, soil_3_key, soil_4_key, soil_5_key, soil_6_key, soil_7_key]
    value = plant_soil_keys[int(plant_name)].get()['Value']
    return value

print(update_plant_soil_value('0'))
