"""
This file contains codeflow suggestion for how the codeflow would work in
the project.
*Add more text*
"""

## Get class module COT_Signal for communication
from plant_modules import COT_Signal

token = "Insert token"

## Keys
soilsensor_key = COT_Signal()
temperature_key = COT_Signal()
humidity_key = COT_Signal()
uvsensor_key = COT_Signal()
luxsensor_key = COT_Signal()
pump_state_key = COT_Signal()
ultrasonic_key = COT_Signal()

def watering():
    ## Here is where it'll pump water to flower if needed based on soil sensor
    print("Water Water")
    
while True:
    print("Yo")