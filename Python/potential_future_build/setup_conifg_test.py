from plant_modules_v2 import COT_Signal
import json

token2 = '[Insett token]'

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
    To set up a dictionary to be ready for use. Only used when needed
    '''
    
    # Open stored dictionary
    with open('plant_dictionaries_v2.json') as json_file:
        dictionaries = json.load(json_file)
        
    # Getting some variable values from Circus of Things
    new_plant = bool(new_plant_configuration_key2.get()['Value'])
    save_configuration = bool(save_configuration_key2.get()['Value'])
    plant_number = str(int(plant_number_key2.get()['Value']))
    store_plant_number = bool(int(plant_number_key2.get()['Value']))  
    
    # If configuration doesn't exist in dictionary and user don't want a new plant, raise an error
    if plant_number not in dictionaries and new_plant == False:
        error_key2.put(1)
        return error_key2.get()['Value']
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
        default = new_default_dictionary()
        #Checks if user want to save configuration.
        save_configuration = bool (save_configuration_key2.get()['Value'])
     
    # If user want to save configuration, reset variables and save the dictionary
    if(new_plant == True and save_configuration == True):
        new_plant_configuration_key2.put(0)
        save_configuration_key2.put(0)
        error_key2.put(0)
        
        dictionaries[plant_number] = default
        with open('plant_dictionaries_v2.json', 'w') as json_file:
            json.dump(dictionaries,json_file)
      
        return default
    
    else:
        soil_requirement_key2.put(dictionaries[plant_number]['soil_requirement'])
        light_requirement_key2.put(dictionaries[plant_number]['light_requirement'])
        temperature_maximum_key2.put(dictionaries[plant_number]['temperature_maximum'])
        temperature_minimum_key2.put(dictionaries[plant_number]['temperature_minimum'])
        humidity_requirement_key2.put(dictionaries[plant_number]['humidity_requirement'])
        return dictionaries[plant_number]

def plant_configuration(plant_number,plant_configuration):
    #plant_number is string, plant_configuration is a single dictionary, and save_configuration is int
    with open('plant_dictionaries_v2.json') as json_file:
        dictionaries = json.load(json_file)
        
    plant_configuration['soil_requirement'] = soil_requirement_key2.get()['Value']
    plant_configuration['light_requirement'] = light_requirement_key2.get()['Value']
    plant_configuration['temperature_maximum'] = temperature_maximum_key2.get()['Value']
    plant_configuration['temperature_minimum'] = temperature_minimum_key2.get()['Value']
    plant_configuration['humidity_requirement'] = humidity_requirement_key2.get()['Value'] 
    
    with open('plant_dictionaries_v2.json','w') as json_file:
        dictionaries[plant_number] = plant_configuration
        json.dump(dictionaries, json_file)
        
    save_configuration_key2.put(0)    
    
    soil_requirement_key2.put(plant_configuration['soil_requirement'])
    light_requirement_key2.put(plant_configuration['light_requirement'])
    temperature_maximum_key2.put(plant_configuration['temperature_maximum'])
    temperature_minimum_key2.put(plant_configuration['temperature_minimum'])
    humidity_requirement_key2.put(plant_configuration['humidity_requirement'])   

plant_dictionary = plant_setup()
print(plant_dictionary)
 
while True:
    new_plant = new_plant_configuration_key2.get()['Value']
    save_configuration = save_configuration_key2.get()['Value']
    
    if new_plant == 1 or plant_dictionary == 1:  
        plant_dictionary = plant_setup()
        store_plant_number = str(int(plant_number_key2.get()['Value']))
        
    if (save_configuration == 1 and type(plant_dictionary) is dict) and (int(plant_dictionary['plant_number']) == plant_number_key2.get()['Value']):
        plant_number = plant_number_key2.get()['Value']
        plant_configuration(plant_number, plant_dictionary)
    else:
        error_key2.put(2)