# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 15:39:59 2021

@author: si_ve
"""
from datetime import *
from CoT import *


#### Plant thirst levels ####---------------------------------------------------------------------------
# All values have a moisture range from 0% too 100%
# water need thresholds
soil_threshold_hella_thirsty = 90
soil_threshold_normal_thirsty = 60
soil_threshold_kinda_thirsty = 400
soil_threshold_low_thirsty = 250
soil_threshold_cactus = 100


# water need dict
water_requirement = {'hella thirsty':soil_threshold_hella_thirsty,
                     'normal thirsty':soil_threshold_normal_thirsty,
                     'kinda thirsty':soil_threshold_kinda_thirsty,
                     'low thirsty':soil_threshold_low_thirsty,
                     'cactus':soil_threshold_cactus
                     }



#### Plant light levels ####--------------------------------------------------------------------------

# Light requirement thresholds
light_threshold_cactus = 1000
light_threshold_bright = 700
light_threshold_shadow = 400


# light need dict
light_requirement = {'cactus':light_threshold_cactus,
                     'bright':light_threshold_bright,
                     'shadow':light_threshold_shadow
                     }

#### Plant temp levels ####---------------------------------------------------------------------------

# Temp ranges  (All values are in celcius where the first value of the list is the minimum temp the plant
#               can tolarate and last value of the list is the bare maximum temp.)
temp_range_cactus = [7,29]
temp_range_room = [16,26]
temp_range_picky = [20,24]


# Temp range dict
temp_range = {'cactus':temp_range_cactus,
              'room':temp_range_room,
              'picky':temp_range_picky
              }



#### Plant humidity levels ####------------------------------------------------------------------------

# humidity ranges (All values are in relative humidity [% rH],
#                they are the minimum humidity level where the plant trives)
humid_threshold_moist = 50
humid_threshold_normal = 30
humid_threshold_cactus = 20


# humid threshold dict
humid_requirement = {'moist':humid_threshold_moist,
                     'normal':humid_threshold_normal,
                     'cactus':humid_threshold_cactus
                     }


#### plant status dict (Up too 8 plants.) ####---------------------------------------------------------

# example: get soil value of plant 0 ---> plant[0]['soil_value'] gives the value(number) of plant 0.
plant = {0:
         {'water_requirement':water_requirement['hella thirsty'],
          'soil_value':soil_key.get()["Value"],
          'last_soil_measure':soil_key.get()["LastValueTime"],
          'water':False, # Values from 0 - 5 wich describes how much water the plant is getting from signal
          'last_water':pump_0_key.get()['LastValueTime'],
          'light_requirement':light_requirement['bright'],
          'light_value':light_key.get()["Value"],
          'light':False,
          'temp_range':temp_range['room'],
          'temp_value':temp_key.get()['Value'],
          'humid_requirment':humid_requirement['normal'],
          'humid_value':humid_key.get()['Value']
          },
         1:{},
         2:{},
         3:{},
         4:{},
         5:{},
         6:{},
         7:{}
         }

print(datetime.fromtimestamp(plant[0]['last_water']/1000).strftime('%Y-%m-%d %H:%M:%S'))
print(plant[0]['temp_value'])
print(plant[0]['water_requirement'])
