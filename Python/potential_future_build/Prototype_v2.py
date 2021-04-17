"""
This file contains codeflow suggestion for how the codeflow would work in
the project.
*Add more text*
"""
## Get class module COT_Signal for communication
from plant_modules import COT_Signal
token1 = "Insert token"
token2 = "Insert token"

## Keys for token1
soilsensor_key1 = COT_Signal()
temperature_key1 = COT_Signal()
humidity_key1 = COT_Signal()
uvsensor_key1 = COT_Signal()
luxsensor_key1 = COT_Signal()
pump_state_key1 = COT_Signal()
ultrasonic_key1 = COT_Signal()

## Keys for token2
soil_requirement_key2 = COT_Signal()


def plant_calibration():
    """
    To calibrate the system to fit for the plant the code is currently working with. 
    Should be able to update the dictionary & save new configuration. 
    """
    print("This is fine")
    
def watering():
    soilsensor_value  = soilsensor_key1.get()["Value"]
    if soilsensor_value < soil_requirement_key2.get()["Value"]: # and last time watering happened is more than 30 min
        pump_state_key1.put(1)
    else:
        pump_state_key1.put(0)

def plant_lights():
    """
    If the plants haven't got enough sunlight, then it should turn on the plant lights
    """
    
while True:
    """
    Systems main code to be run. 
    """
