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


# ----------------------------------------------------------------------------------------------------------------------

# First time python is run (reboot system)
plant_dictionary = plant_modules.plant_setup()
print(plant_dictionary)

while True:
    """
    System main code to be run.
    """
    # Always checks on if user wants a new plant(create a new or switch), or save a new configuration.
    new_plant = CoT.new_plant_configuration_key2.get()['Value']
    save_configuration = CoT.save_configuration_key2.get()['Value']

    # Will be true if user wants to switch plant or create a new one. It will also be run if plant_dictionary does not have any dictionary
    if new_plant == 1 or plant_dictionary == 1:
        plant_dictionary = plant_modules.plant_setup()

    # Will be true if user wants to save new configuration to current plant configuration.
    if (save_configuration == 1 and type(plant_dictionary) is dict) and (int(plant_dictionary['plant_number']) == CoT.plant_number_key2.get()['Value']):
        plant_number = CoT.plant_number_key2.get()['Value']
        plant_modules.plant_configuration(plant_number, plant_dictionary)

    # If user wanted to save configuration, but pushed on wrong plant in CoT,
    # then we'll update the signal to let user know which configuration the system is currently working with
    # and reset save_configuration.
elif (save_configuration == 1) and (int(plant_dictionary['plant_number']) != CoT.plant_number_key2.get()['Value']):
            CoT.plant_number_key2.put(plant_dictionary['plant_number'])
            CoT.save_configuration_key2.put(0)

    #### Update sensor values ####--------------------------------------------------------------------------------------
    for plant_name in range(0, 1): # When done: range(0, len(plant_dictionary)): It wil then run trough all the plants
        plant_modules.update_plant_soil_value(plant_name)
        plant_modules.update_plant_water_state(plant_name)

        #### Check sensors ####-----------------------------------------------------------------------------------------

        plant_modules.plant_soil_check(plant_name)

        #### Water and light ####---------------------------------------------------------------------------------------
        plant_modules.water(plant_name)



    #### Serial monitor ####--------------------------------------------------------------------------------------------
    print('##########################################################')
    print('PLANT STATUSES:')
    for plant_name in range(0, 2):
        print('\n  Plant', str(plant_name) +':')
        print('  Soil:', int(plant_dictionary[str(plant_name)]['soil_value']), '    Threshold:', plant_dictionary[str(plant_name)]['water_requirement'])
        print('  Pump:', plant_dictionary[str(plant_name)]['water'], '  Last given water:', datetime.fromtimestamp(plant_dictionary[str(plant_name)]['last_water']).strftime('%H:%M:%S %d/%m-%Y'))

    print('##########################################################')




    time.sleep(1)
