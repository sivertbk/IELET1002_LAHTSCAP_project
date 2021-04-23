# @Date:   2021-04-21T14:03:41+02:00
# @Last modified time: 2021-04-21T17:34:33+02:00



from CoT import COT_Signal
import json

token2 = 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1Nzk0In0.nqXSqXGe2AXcNm4tdMUl7qIzmpAEXwr7UPKf5AtYx4k'

## Keys for token2
new_plant_configuration_key2 = COT_Signal('10620', token2)
plant_number_key2 = COT_Signal('7801', token2)
soil_requirement_key2 = COT_Signal('5893', token2)
light_requirement_key2 = COT_Signal('22405', token2)
temperature_maximum_key2 = COT_Signal('32424', token2)
temperature_minimum_key2 = COT_Signal('10771', token2)
humidity_requirement_key2 = COT_Signal('5950', token2)
save_configuration_key2 = COT_Signal('24567', token2)
active_status_key2 = COT_Signal('3904', token2)

def new_default_dictionary():
    """
    A default plant dictionary used for new plant configurations.
    Everytime this is run, the dictionary will get updated values for user controlled variables.
    """
    default = {'plant_number':plant_number_key2.get()['Value'],
               'active_status':active_status_key2.get()['Value'],
               'soil_requirement':soil_requirement_key2.get()['Value'],
               'light_requirement':light_requirement_key2.get()['Value'],
               'temperature_maximum':temperature_maximum_key2.get()['Value'],
               'temperature_minimum':temperature_minimum_key2.get()['Value'],
               'humidity_requirement':humidity_requirement_key2.get()['Value']
               }
    return default

def plant_setup():
    '''
    Used for the first time to get the dictionaries stored in json_file. 
    Afterwards, it's used for whenever the user wants to store a new configuration.
    (And also to see what's already stored)
    '''
    
    with open('plant_dictionaries_v2.json') as json_file:
        dictionaries = json.load(json_file)
    
    plant_number = str(plant_number_key2.get()['Value'])
    
    if plant_number not in dictionaries:
        dictionaries[plant_number] = new_default_dictionary()
        
    else:
        plant_number_key2.put(dictionaries[plant_number]['plant_number'])
        active_status_key2.put(dictionaries[plant_number]['active_status'])
        soil_requirement_key2.put(dictionaries[plant_number]['soil_requirement'])
        light_requirement_key2.put(dictionaries[plant_number]['light_requirement'])
        temperature_maximum_key2.put(dictionaries[plant_number]['temperature_maximum'])
        temperature_minimum_key2.put(dictionaries[plant_number]['temperature_minimum'])
        humidity_requirement_key2.put(dictionaries[plant_number]['humidity_requirement'])
    
    with open('plant_dictionaries_v2.json', 'w') as json_file:
        json.dump(dictionaries, json_file)   
        
    new_plant_configuration_key2.put(0)
    
    return dictionaries

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
    plant_configuration['active_status'] = active_status_key2.get()['Value']

    # Save the updated dictionary to json file.
    with open('plant_dictionaries_v2.json','w') as json_file:
        dictionaries[plant_number] = plant_configuration
        json.dump(dictionaries, json_file)

    # Reset save_configuration
    save_configuration_key2.put(0)

if __name__=="__main__":

    # First time python is run (reboot system)
    plant_dictionary = plant_setup()
    print(plant_dictionary)

    while True:
        # Always checks on if user wants a new plant(create a new or switch), or save a new configuration.
        new_plant = new_plant_configuration_key2.get()['Value']
        save_configuration = save_configuration_key2.get()['Value']
        
        # Whenever user wants to store a new configuration or look at what's already stored.
        if (new_plant == 1):
            plant_dictionary = plant_setup()

        # Will be true if user wants to save new configuration.
        if (save_configuration == 1):
            plant_number = str(plant_number_key2.get()['Value'])
            plant_configuration(plant_number, plant_dictionary[plant_number])

        #Timer that will open json_file and store the dictionary
        print(plant_dictionary)