# @Date:   2021-04-21T14:03:41+02:00
# @Last modified time: 2021-04-21T17:34:33+02:00



from CoT import COT_Signal
import json

token2 = 'Insert token'

## Keys for token2
new_plant_configuration_key2 = COT_Signal('10620', token2)
plant_number_key2 = COT_Signal('7801', token2)
soil_requirement_key2 = COT_Signal('5893', token2)
light_requirement_key2 = COT_Signal('22405', token2)
temperature_maximum_key2 = COT_Signal('32424', token2)
temperature_minimum_key2 = COT_Signal('10771', token2)
humidity_requirement_key2 = COT_Signal('5950', token2)
save_configuration_key2 = COT_Signal('24567', token2)
error_key2 = COT_Signal('3904', token2)

def new_default_dictionary():
    """
    A default plant dictionary used for new plant configurations.
    Everytime this is run, the dictionary will get updated values for user controlled variables.
    """
    default = {'plant_number':plant_number_key2.get()['Value'],
            'soil_requirement':soil_requirement_key2.get()['Value'],
           'light_requirement':light_requirement_key2.get()['Value'],
           'temperature_maximum':temperature_maximum_key2.get()['Value'],
           'temperature_minimum':temperature_minimum_key2.get()['Value'],
           'humidity_requirement':humidity_requirement_key2.get()['Value']
           }
    return default

def plant_setup():
    '''
    To set up a dictionary to be ready for use.
    Used whenever user wants to create a new plant configuration or switch to a different plant.
    '''

    # Open stored dictionary
    with open('plant_dictionaries_v2.json') as json_file:
        dictionaries = json.load(json_file)

    # Getting some variable values from Circus of Things
    new_plant = bool(new_plant_configuration_key2.get()['Value'])
    save_configuration = bool(save_configuration_key2.get()['Value'])
    plant_number = str(int(plant_number_key2.get()['Value']))

    # If configuration doesn't exist in dictionary and user don't want a new plant, raise an error
    if plant_number not in dictionaries and new_plant == False:
        error_key2.put(1)
        return error_key2.get()['Value']

    # If user want's a new plant and configuration doesn't exist, make sure user can create a new plant.
    elif plant_number not in dictionaries and new_plant == True:
        save_configuration = False
        save_configuration_key2.put(0)

    # If the plant exists in dictionaries, reset some of the variables
    elif plant_number in dictionaries:
        save_configuration = False
        save_configuration_key2.put(0)
        new_plant = False
        new_plant_configuration_key2.put(0)

    # As long as user wants a new plant, but not save the configuration,
    # the user can edit the configuration
    while(new_plant == True and save_configuration == False):

        # updates the configurations for every loop
        default = new_default_dictionary()

        #Checks if user want to save configuration.
        save_configuration = bool (save_configuration_key2.get()['Value'])

    # If user want to save configuration, reset variables to zero and save the dictionary
    if(new_plant == True and save_configuration == True):
        new_plant_configuration_key2.put(0)
        save_configuration_key2.put(0)
        error_key2.put(0)

        dictionaries[plant_number] = default
        with open('plant_dictionaries_v2.json', 'w') as json_file:
            json.dump(dictionaries,json_file)

        return default

    # If user wanted to switch to a different plant configuration, make sure to update
    # circus of things with the new configuration and return the new dictionary.
    else:
        soil_requirement_key2.put(dictionaries[plant_number]['soil_requirement'])
        light_requirement_key2.put(dictionaries[plant_number]['light_requirement'])
        temperature_maximum_key2.put(dictionaries[plant_number]['temperature_maximum'])
        temperature_minimum_key2.put(dictionaries[plant_number]['temperature_minimum'])
        humidity_requirement_key2.put(dictionaries[plant_number]['humidity_requirement'])
        return dictionaries[plant_number]


# plant_number is string, plant_configuration is a single dictionary.
def plant_configuration(plant_number,plant_configuration):
    """
    This function is used for whenever the user wants to change some of the configuration to an already exisiting plant
    """
    # Get our stored dictionary of every plant configuration user has made.
    with open('plant_dictionaries_v2.json') as json_file:
        dictionaries = json.load(json_file)

    # Update all values to every key that is based on user input.
    plant_configuration['soil_requirement'] = soil_requirement_key2.get()['Value']
    plant_configuration['light_requirement'] = light_requirement_key2.get()['Value']
    plant_configuration['temperature_maximum'] = temperature_maximum_key2.get()['Value']
    plant_configuration['temperature_minimum'] = temperature_minimum_key2.get()['Value']
    plant_configuration['humidity_requirement'] = humidity_requirement_key2.get()['Value']

    # Save the updated dictionary to json file.
    with open('plant_dictionaries_v2.json','w') as json_file:
        dictionaries[plant_number] = plant_configuration
        json.dump(dictionaries, json_file)

    # Reset save_configuration
    save_configuration_key2.put(0)

    # Update Circus of Things signals (Might be possible to delete this one)
    soil_requirement_key2.put(plant_configuration['soil_requirement'])
    light_requirement_key2.put(plant_configuration['light_requirement'])
    temperature_maximum_key2.put(plant_configuration['temperature_maximum'])
    temperature_minimum_key2.put(plant_configuration['temperature_minimum'])
    humidity_requirement_key2.put(plant_configuration['humidity_requirement'])

if __name__=="__main__":

    # First time python is run (reboot system)
    plant_dictionary = plant_setup()
    print(plant_dictionary)

    while True:
        # Always checks on if user wants a new plant(create a new or switch), or save a new configuration.
        new_plant = new_plant_configuration_key2.get()['Value']
        save_configuration = save_configuration_key2.get()['Value']

        # Will be true if user wants to switch plant or create a new one. It will also be run if plant_dictionary does not have any dictionary
        if new_plant == 1 or plant_dictionary == 1:
            plant_dictionary = plant_setup()
            store_plant_number = str(int(plant_number_key2.get()['Value']))

        # Will be true if user wants to save new configuration.
        if (save_configuration == 1 and type(plant_dictionary) is dict) and (int(plant_dictionary['plant_number']) == plant_number_key2.get()['Value']):
            plant_number = plant_number_key2.get()['Value']
            plant_configuration(plant_number, plant_dictionary)

        # If user wanted to save configuration, but pushed on wrong plant in CoT,
        # then we'll update the signal to let user know which configuration the system is currently working with
        # and reset save_configuration.
        elif (save_configuration == 1) and (int(plant_dictionary['plant_number']) != plant_number_key2.get()['Value']):
                plant_number_key2.put(plant_dictionary['plant_number'])
                save_configuration_key2.put(0)
