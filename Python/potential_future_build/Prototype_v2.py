# @Date:   2021-04-21T14:03:41+02:00
# @Last modified time: 2021-04-23T12:58:40+02:00



"""
This file contains codeflow suggestion for how the codeflow would work in
the project.
*Add more text*
"""
import plant_modules
import CoT
import json
from datetime import *
import time


# ----------------------------------------------------------------------------------------------------------------------

# First time python is run (reboot system)
plant_dictionary = plant_modules.plant_setup()
'''
for plant_name in range(1,len(plant_dictionary)):
    plant_dictionary[str(plant_name)]['last_water'] = int(time.time())
print(plant_dictionary)
'''

"""
System main code to be run.
"""


while True:
    # Always checks on if user wants a new plant(create a new or switch), or save a new configuration.
    new_plant = plant_modules.new_plant_configuration_key2.get()['Value']
    save_configuration = plant_modules.save_configuration_key2.get()['Value']
    
    # Whenever user wants to store a new configuration or look at what's already stored.
    if (new_plant == 1):
        plant_dictionary = plant_modules.plant_setup()
        
    # Will be true if user wants to save new configuration.
    if (save_configuration == 1):
        plant_number = str(plant_modules.plant_number_key2.get()['Value'])
        plant_modules.plant_configuration(plant_number, plant_dictionary[plant_number])

    #Timer that will open json_file and store the dictionary
    #print(plant_dictionary)

    #### Update sensor values ####--------------------------------------------------------------------------------------
    for plant_name in range(1, 3): # When done: range(0, len(plant_dictionary)): It wil then run trough all the plants
        
        plant_dictionary = plant_modules.update_plant_soil_value(plant_dictionary, plant_name)
        
        plant_dictionary = plant_modules.update_plant_water_state(plant_dictionary, plant_name)
        

        #### Check sensors ####-----------------------------------------------------------------------------------------

        plant_dictionary = plant_modules.plant_soil_check(plant_dictionary, plant_name)
        
        #### Water and light ####---------------------------------------------------------------------------------------
        plant_modules.water(plant_dictionary, plant_name)
        
    
    

    #### Serial monitor ####--------------------------------------------------------------------------------------------
    print('##########################################################')
    print('PLANT STATUSES:')
    for plant_name in range(1, 3):
        print('\n  Plant', str(plant_name) +':')
        print('  Soil:', int(plant_dictionary[str(plant_name)]['soil_value']), '    Threshold:', int(plant_dictionary[str(plant_name)]['soil_requirement']))
        print('  Pump:', plant_dictionary[str(plant_name)]['water'], '  Last given water:', datetime.fromtimestamp(plant_dictionary[str(plant_name)]['last_water']).strftime('%H:%M:%S %d/%m-%Y'))

    print('##########################################################')


    with open('plant_dictionaries_v2.json', 'w') as json_file:
        json.dump(plant_dictionary, json_file)

    time.sleep(1)
