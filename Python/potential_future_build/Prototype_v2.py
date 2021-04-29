# @Date:   2021-04-21T14:03:41+02:00
# @Last modified time: 2021-04-29T15:06:37+02:00



"""
This file contains codeflow suggestion for how the codeflow would work in
the project.
*Add more text*
"""
import plant_modules
import CoT
import serial_messages
import json
from datetime import datetime
import time


# ----------------------------------------------------------------------------------------------------------------------

# First time python is run (reboot system)
plant_dictionary = plant_modules.plant_setup()

"""
System main code to be run.
"""


while True:
    # Always checks on if user wants a new plant(create a new or switch), or save a new configuration.
    new_plant = CoT.new_plant_configuration_key2.get()['Value']
    save_configuration = CoT.save_configuration_key2.get()['Value']

    # Whenever user wants to store a new configuration or look at what's already stored.
    if (new_plant == 1):
        plant_dictionary = plant_modules.plant_setup()

    # Will be true if user wants to save new configuration.
    if (save_configuration == 1):
        plant_number = str(CoT.plant_number_key2.get()['Value'])
        plant_modules.plant_configuration(plant_number, plant_dictionary[plant_number])

    #### Main loop ####-------------------------------------------------------------------------------------------------
    for plant_name in range(1, 9):

        if plant_dictionary[str(plant_name)]['active_status']: # Only run if plant is active

            #### Update sensor values ####------------------------------------------------------------------------------

            plant_dictionary = plant_modules.update_plant_sensor_values_v2(plant_dictionary, plant_name)
            plant_dictionary = plant_modules.update_plant_system_states(plant_dictionary, plant_name)

            #### Check sensors ####-------------------------------------------------------------------------------------

            plant_dictionary = plant_modules.soil_check(plant_dictionary, plant_name)
            plant_dictionary = plant_modules.lux_check(plant_dictionary, plant_name)
            plant_dictionary = plant_modules.checking_temperature(plant_dictionary, plant_name)
            plant_dictionary = plant_modules.checking_humidity(plant_dictionary, plant_name)
            plant_dictionary = plant_modules.checking_water_tank_volume(plant_dictionary, plant_name)

            #### Put updated states to CoT ####-------------------------------------------------------------------------

            plant_dictionary = plant_modules.put_system_states_to_CoT(plant_dictionary, plant_name)

        else:
            continue


    #### Serial monitor ####--------------------------------------------------------------------------------------------
    print('##########################################################')
    print('PLANT STATUSES:                           CLOCK:', datetime.fromtimestamp(int(time.time())).strftime('%H:%M:%S'))
    for plant_name in range(1, 9):
        if plant_dictionary[str(plant_name)]['active_status']:
            print('\n  Plant', str(plant_name) +':     ', serial_messages.plant_checktime_left(str(plant_name)))
            print('  Soil:', int(plant_dictionary[str(plant_name)]['soil_value']), '     Threshold:', int(plant_dictionary[str(plant_name)]['soil_requirement']))
            print('  Pump:', plant_dictionary[str(plant_name)]['pump_state'], '      Last given water:', datetime.fromtimestamp(plant_dictionary[str(plant_name)]['last_water']).strftime('%H:%M:%S %d/%m-%Y'))

            print('\n  Lux:', int(plant_dictionary[str(plant_name)]['lux_value']), '   Threshold:', int(plant_dictionary[str(plant_name)]['lux_requirement']))
            print('  Light:', plant_dictionary[str(plant_name)]['light_state'])

        else:
            continue

    print('##########################################################')


    with open('plant_dictionaries_v2.json', 'w') as json_file:
        json.dump(plant_dictionary, json_file)

    #time.sleep(1)
