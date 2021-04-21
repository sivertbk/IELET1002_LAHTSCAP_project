'''
This file contains modules & functions. 
'''
import requests
import json
from datetime import *


## A class module that will connect a variable to Circus of Things.
class COT_Signal:
    def __init__(self, key, token):
        '''
        Connect the variable to a signal key and token from Circus of Things.
        '''
        self.key = key
        self.token = token
        self.payload = {'Key':self.key, 'Token':self.token}

    def get(self):
        '''
        Read (get) the signal value that is stored in Circus of Things.
        '''
        response = requests.get('https://circusofthings.com/ReadValue',
                                params = self.payload)
        response = json.loads(response.content)
        return response

    def put(self, value):
        '''
        Write (put) a new value to the signal that should be stored in Circus of Things.
        '''
        self.value = value
        self.payload['Value'] = value
        response = requests.put('https://circusofthings.com/WriteValue',
                                params = self.payload,
                                data = json.dumps(self.payload),
                                headers = {'Content-Type':'application/json'})



soil_time_tracker = {'0':[],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[]}
soil_control = {'0':False,'1':False,'2':False,'3':False,'4':False,'5':False,'6':False,'7':False}
soil_over_threshold = {'0':True,'1':True,'2':True,'3':True,'4':True,'5':True,'6':True,'7':True}




def plant_last_water_timestamp(plant_name, timeformat):
    """
    This function takes 2 arguments and returns a timestamp for when given plant got water last time.
    Choose plant and what timeformat it should return your value as.
    """
    # list of all pump keys for each plant, where the index matches all the plant names.
    plant_pump_keys = [pump_0_key, pump_1_key, pump_3_key, pump_4_key, pump_5_key, pump_6_key, pump_7_key]

    # Calls the last time pump state changed in CoT and stores the value in 'timestamp'.
    if timeformat == ('epoch' or 'unix time'):
        timestamp = plant_pump_keys[int(plant_name)].get()['LastValueTime']/1000
    elif timeformat == 'datetime':
        timestamp = datetime.fromtimestamp(plant_pump_keys[int(plant_name)].get()['LastValueTime']/1000).strftime('%Y-%m-%d %H:%M:%S')
    return timestamp




def update_plant_soil_value(plant_name):
    """
    This function takes the given plant's soil value from CoT and updates the plant dictionary ['soil_value'].
    """
    # list of all soil keys for each plant, where the index matches all the plant names.
    plant_soil_keys = [soil_0_key, soil_1_key, soil_2_key, soil_3_key, soil_4_key, soil_5_key, soil_6_key, soil_7_key]
    plant[str(plant_name)]['soil_value'] = plant_soil_keys[int(plant_name)].get()['Value']
    return




def update_plant_water_state(plant_name):
    """
    This function takes the given plant's water state from CoT and updates the plant dictionary ['water'].
    """
    plant_pump_keys = [pump_0_key, pump_1_key, pump_3_key, pump_4_key, pump_5_key, pump_6_key, pump_7_key]
    if plant_pump_keys[int(plant_name)].get()['Value'] == 1:
        plant[str(plant_name)]['water'] = True
    elif plant_pump_keys[int(plant_name)].get()['Value'] == 0:
        plant[str(plant_name)]['water'] = False
    return




def plant_soil_check(plant_name):
    """
    Function which takes the plant name as an argument and checks if the plant need water or not.
    When the plant need water it changes the plants water status to True
    """
    current_time = int(time.time()) # current time in epoch
    soil_value = plant[str(plant_name)]['soil_value']
    Threshold = plant[str(plant_name)]['water_requirement']
    last_water = plant[str(plant_name)]['last_water']
    water_interval = 10 # 12 Hours interval = 43200 seconds(25 seconds offset/lag)
    control_wait_time = 30 # control wait time 30 minutes = 1800 seconds
    #global soil_control, soil_time_tracker

    if (soil_value < Threshold) and ((current_time - last_water) > water_interval):
        soil_over_threshold[str(plant_name)] = False
        if soil_control[str(plant_name)]:
            if (current_time - soil_time_tracker[str(plant_name)]) > control_wait_time:
                soil_control[str(plant_name)] = False
                soil_time_tracker[str(plant_name)] = 0
                plant[str(plant_name)]['water'] = True
                return print('watering plant',str(plant_name)+'!')
            else:
                return
        else:
            print('Plant', str(plant_name), 'soil control in progress! If pass, water in', control_wait_time, 'seconds.')
            soil_time_tracker[str(plant_name)] = int(time.time())
            soil_control[str(plant_name)] = True

    else:
        soil_control[str(plant_name)] = False
        soil_over_threshold[str(plant_name)] = True
        return # print('Plant', plant_name, 'soil is good enough :D')
    return




def water(plant_name):
    plant_pump_keys = [pump_0_key, pump_1_key, pump_3_key, pump_4_key, pump_5_key, pump_6_key, pump_7_key]
    if plant[str(plant_name)]['water']:
        plant[str(plant_name)]['last_water'] = int(time.time())
        return plant_pump_keys[int(plant_name)].put(1)
    else:
        return


if __name__ == "__main__":
    print("Oh no")
    
