'''
This file is used for a plants configuration.
*Add more text*
'''

import datetime
from plant_modules import COT_Signal

token2 = 'Insert token'

new_plant_key2 = COT_Signal()
plant_number_key2 = COT_Signal()
soil_requirement_key2 = COT_Signal()
light_requirement_key2 = COT_Signal()
temperature_maximum_key2 = COT_Signal()
temperature_minimum_key2 = COT_Signal()
humidity_requirement_key2 = COT_Signal()



"""
plant variable is a dictionary that contains a dictionary of a plants configuration.
Here one can store new configuration for new plants and get already existing configuration for plants that falls
within the same category.
"""
plant = {'0':
         {'soil_requirement':soil_requirement_key2.get()['Value'],
          'light_requirement':light_requirement_key2.get()['Value'],
          'temperature_maximum':temperature_maximum_key2.get()['Value'],
          'temperature_minimum':temperature_minimum_key2.get()['Value'],
          'humidity_requirement':humidity_requirement_key2.get()['Value']
          }
         }


if __name__ == '__main__':

    print(datetime.fromtimestamp(plant['0']['last_water']/1000).strftime('%Y-%m-%d %H:%M:%S'))
    print(plant['0']['temp_value'])
    print(plant['0']['water_requirement'])
