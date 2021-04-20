# @Date:   2021-04-15T14:35:02+02:00
# @Last modified time: 2021-04-20T23:13:42+02:00



from datetime import *
from CoT import *


#### Options of water requirement for a plant ####---------------------------------------------------------------------------
# All values have a moisture range from 0% to 100%
# Dictionary with thresholds value of how much water a plants need based on its soil moisture.
water_requirement_threshold = {'high moisture':90,
                               'decent moisture':60,
                               'normal moisture':40,
                               'low moisture':25,
                               'cactus':10
                               }


#### Options of light requirements for a plant ####--------------------------------------------------------------------------
# Dictionary with thresholds value of how much light the plant needs.
light_requirement_threshold = {'cactus':1000,
                               'bright':700,
                               'shadow':400
                               }

#### Options of temperature range for a plant ####---------------------------------------------------------------------------
# Dictionary with [min, max] temperature thresholds for a plant in celcius.
temp_range = {'cactus':[7,29],
              'room':[16,26],
              'picky':[20,24]
              }

#### Options of humid requirement for a plant ####------------------------------------------------------------------------
# Dictionary with threshold value for minimum humidity (in [% rH]) where a plant thrives
humid_requirement_threshold = {'moist':50,
                               'normal':30,
                               'cactus':20
                               }

#### Dictionary of up to 8 plants with it's each own dictionary of the plants status ####
# example: get soil value of plant 0 ---> plant['0']['soil_value'] gives the value(number) of plant '0'.
plant = {'0':
         {'water_requirement':water_requirement_threshold['high moisture'],
          'soil_value':soil_0_key.get()['Value'],
          'last_soil_measure':soil_0_key.get()['LastValueTime'],
          'water':False, # Values from 0 - 5 wich describes how much water the plant is getting from signal
          'last_water':int(pump_0_key.get()['LastValueTime']/1000),
          'light_requirement':light_requirement_threshold['bright'],
          'light_value':light_0_key.get()['Value'],
          'light':False,
          'temp_range':temp_range['room'],
          'temp_value':temp_0_key.get()['Value'],
          'humid_requirment':humid_requirement_threshold['normal'],
          'humid_value':humid_0_key.get()['Value']
          },
         '1':
         {'water_requirement':water_requirement_threshold['high moisture'],
          'soil_value':soil_1_key.get()['Value'],
          'last_soil_measure':0,
          'water':False,
          'last_water':int(pump_1_key.get()['LastValueTime']/1000),
          'light_requirement':light_requirement_threshold['bright'],
          'light_value':'empty',
          'light':False,
          'temp_range':temp_range['room'],
          'temp_value':'empty',
          'humid_requirment':humid_requirement_threshold['normal'],
          'humid_value':'empty'
          },
         '2':{},
         '3':{},
         '4':{},
         '5':{},
         '6':{},
         '7':{}
         }


if __name__ == "__main__":

    print(datetime.fromtimestamp(plant['0']['last_water']).strftime('%Y-%m-%d %H:%M:%S'))
    print(plant['0']['last_water'])
    print(plant['0']['soil_value'])
