from datetime import *
from CoT import *


#### Options of water requirement for a plant ####---------------------------------------------------------------------------
# All values have a moisture range from 0% to 100%
# Dictionary with thresholds value of how much water a plants need based on its soil moisture. 
water_requirement = {'high moisture':90,
                     'decent moisture':60,
                     'normal moisture':40,
                     'low moisture':25,
                     'cactus':10
                     }



#### Options of light requirements for a plant ####--------------------------------------------------------------------------
# Dictionary with thresholds value of how much light the plant needs. 
light_requirement = {'cactus':1000,
                     'bright':700,
                     'shadow':400
                     }

#### Options of temperature range for a plant ####---------------------------------------------------------------------------
# Dictionary with [min, max] temperature thresholds for a plant
temp_range = {'cactus':[7,29],
              'room':[16,26],
              'picky':[20,24]
              }


#### Options of humid requirement for a plant ####------------------------------------------------------------------------
# Dictionary with threshold value for minimum humidity (in [% rH]) where a plant thrives
humid_requirement = {'moist':50,
                     'normal':30,
                     'cactus':20
                     }


#### Dictionary of up to 8 plants with it's each own dictionary of the plants status ####--------------------------------------------------------------------------

# example: get soil value of plant 0 ---> plant[0]['soil_value'] gives the value(number) of plant 0.
plant = {0:
         {'water_requirement':water_requirement['high moisture'],
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


if __name__ == "__main__":
    
    print(datetime.fromtimestamp(plant[0]['last_water']/1000).strftime('%Y-%m-%d %H:%M:%S'))
    print(plant[0]['temp_value'])
    print(plant[0]['water_requirement'])
