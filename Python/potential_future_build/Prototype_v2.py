"""
This file contains codeflow suggestion for how the codeflow would work in
the project.
*Add more text*
"""
## Get class module COT_Signal for communication
from plant_modules import COT_Signal
import json

token1 = 'token1'
token2 = 'token2'

## Keys for token1
soilsensor_key1 = COT_Signal('key1-1', token1)
temperature_key1 = COT_Signal('key2-1',token1)
humidity_key1 = COT_Signal('key3-1',token1)
uvsensor_key1 = COT_Signal('key4-1',token1)
luxsensor_key1 = COT_Signal('key5-1',token1)
pump_state_key1 = COT_Signal('key6-1',token1)
ultrasonic_key1 = COT_Signal('key7-1',token1)

## Variables connected to keys for token1


## Keys for token2
new_plant_key2 = COT_Signal('key1-2', token2)
plant_number_key2 = COT_Signal('key2-2', token2)
soil_requirement_key2 = COT_Signal('key3-2', token2)
light_requirement_key2 = COT_Signal('key4-2', token2)
temperature_maximum_key2 = COT_Signal('key5-2', token2)
temperature_minimum_key2 = COT_Signal('key6-2', token2)
humidity_requirement_key2 = COT_Signal('key7-2', token2)


def plant_setup(new_plant):
    """
    To set up a dictionary to be ready for use
    """
    
    with open('plant_dictionaries_v2.json') as json_file:
        dictionaries = json.load(json_file)
    
    plant_number = plant_number_key2.get()['Value']
    new_plant = bool (new_plant_key2.get()['Value'])
    
    if new_plant == True:
        print("Make and store new config")
            
    else:
        return dictionaries[str(plant_number)]
    

def plant_dictionary(dictionary = "empty"):
    print('This where we update already made plant configuration') 
    
    
def watering():
    """
    If the soil is too dry, the system will give the plant some more water
    """

def plant_lights():
    """
    If the plants haven't got enough sunlight, then it should turn on the plant lights
    """
    
while True:
    """
    Systems main code to be run. 
    """
    new_plant = bool(new_plant_key2.get()['Value'])
    
    plant_setup(new_plant)