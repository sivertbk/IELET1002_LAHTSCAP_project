from plant_modules_v2 import COT_Signal
import json

token2 = ''

## Keys for token2
new_plant_configuration_key2 = COT_Signal('29963', token2)
plant_number_key2 = COT_Signal('19680', token2)
soil_requirement_key2 = COT_Signal('4884', token2)
light_requirement_key2 = COT_Signal('20181', token2)
temperature_maximum_key2 = COT_Signal('12799', token2)
temperature_minimum_key2 = COT_Signal('23000', token2)
humidity_requirement_key2 = COT_Signal('23114', token2)
save_configuration_key2 = COT_Signal('29935', token2)
error_key2 = COT_Signal('22924', token2)


def plant_setup():
    '''
    To set up a dictionary to be ready for use. Only used when needed
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
    
    # If the plant exists in dictionaries, reset some of the variables
    elif plant_number in dictionaries:
        save_configuration = False
        save_configuration_key2.put(0)
        new_plant = False
        new_plant_configuration_key2.put(0)
    
    # As long as user wants a new plant, but not save the configuration,
    # the user can edit the configuration
    while(new_plant == True and save_configuration == False):
        default = {'soil_requirement':soil_requirement_key2.get()['Value'],
                   'light_requirement':light_requirement_key2.get()['Value'],
                   'temperature_maximum':temperature_maximum_key2.get()['Value'],
                   'temperature_minimum':temperature_minimum_key2.get()['Value'],
                   'humidity_requirement':humidity_requirement_key2.get()['Value']
                   }
        #Checks if user want to save configuration.
        save_configuration = bool (save_configuration_key2.get()['Value'])
     
    # If user want to save configuration, reset variables and save the dictionary
    if(new_plant == True and save_configuration == True):
        new_plant_configuration_key2.put(0)
        save_configuration_key2.put(0)
        error_key2.put(0)
        
        dictionaries[plant_number] = default
        with open('plant_dictionaries_v2.json', 'w') as json_file:
            dictionaries = json.dump(dictionaries,json_file)
        
        return default
    
    else:
        return dictionaries[plant_number]

def plant_configuration():
    print('This where we update already made plant configuration') 
    

