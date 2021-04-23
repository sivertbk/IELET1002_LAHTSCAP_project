# @Date:   2021-04-21T14:03:43+02:00
# @Last modified time: 2021-04-23T17:41:44+02:00



'''
This file is used for a plants configuration.
*Add more text*
'''

import datetime
import CoT
import time

test_dictionary = {'0':
                    {'water_requirement':[],
                    'soil_value':[],
                    'water':True, # Values from 0 - 5 wich describes how much water the plant is getting from signal
                    'last_water':[],
                    'light_requirement':[],
                    'light_value':[],
                    'light':False,
                    'temp_range':[],
                    'temp_value':[],
                    'humid_requirment':[],
                    'humid_value':[]
                    },
                    '1':{},
                    '2':{},
                    '3':{},
                    '4':{},
                    '5':{},
                    '6':{},
                    '7':{}
                    }

if __name__ == "__main__":
    while True:
    #plant_status = CoT.encode_plant_status('0')
    #print(plant_status)

        plant_0_sensor_values = CoT.decode_sensor_values('0')
        print(plant_0_sensor_values)

        time.sleep(2)
