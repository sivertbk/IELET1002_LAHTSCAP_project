# @Date:   2021-04-21T16:31:52+02:00
# @Last modified time: 2021-04-23T17:40:10+02:00

import requests
import json
#import plant_config_v2
from plant_config_v2 import test_dictionary


#### Class module that will connect a variable to Circus of Things. ####------------------------------------------------
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




#### CoT signal array functions ####------------------------------------------------------------------------------------

def encode_plant_status(plant_name):
    """
    This function takes a plant's inputs (pump and grow light) and arranges it to a array ready to be sent to CoT.
    First number in return value represents plant number + 1 so the value always stay the same length.
    """
    #global test_dictionary
    array = [int(plant_name)+1]
    # get pump status and store value in first index of array
    pump = test_dictionary[str(plant_name)]['water']
    if pump:
        pump = 1
    else:
        pump = 0
    array.append(pump)
    # get light status and store value in last index of array
    light = test_dictionary[str(plant_name)]['light']
    if light:
        light = 1
    else:
        light = 0
    array.append(light)
    # make array into a value to be sent
    array = int(str(array[0])+str(array[1])+str(array[2]))
    return array

def decode_sensor_values(plant_name):
    """
    This function takes a plant's outputs (sensor values) as an array an decodes it to a dictionary of sensor values.
    """
    # get sensor value array for plant
    sensor_values = int(plant_sensor_array_list[int(plant_name)])
    # separate digits in sensor value array into list as string
    sensor_values_list = [str(i) for i in str(sensor_values)]
    # arrange all the digits in correct posision in dictionary and convert into integers again.
    sensor_values_dict = {'plant':int(sensor_values_list[0])-1,
                          'soil':int("".join(sensor_values_list[1:4])),
                          'lux':int("".join(sensor_values_list[4:10])),
                          'temp':int("".join(sensor_values_list[10:13])),
                          'humid':int("".join(sensor_values_list[13:16])),
                          'water_level':int("".join(sensor_values_list[16:]))
                          }
    return sensor_values_dict


#### Signal token ####--------------------------------------------------------------------------------------------------

token = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1Nzk0In0.nqXSqXGe2AXcNm4tdMUl7qIzmpAEXwr7UPKf5AtYx4k"


#### Plant setup & configuration keys ####------------------------------------------------------------------------------

## Keys for user input
new_plant_configuration_key2 = COT_Signal('10620', token)
plant_number_key2 = COT_Signal('7801', token)
soil_requirement_key2 = COT_Signal('5893', token)
light_requirement_key2 = COT_Signal('22405', token)
temperature_maximum_key2 = COT_Signal('32424', token)
temperature_minimum_key2 = COT_Signal('10771', token)
humidity_requirement_key2 = COT_Signal('5950', token)
save_configuration_key2 = COT_Signal('24567', token)
error_key2 = COT_Signal('3904', token)

#### Plant sensor and output signal keys ####---------------------------------------------------------------------------

# Plant 0 keys
soil_0_key = COT_Signal("4991", token)
pump_0_key = COT_Signal('32607', token)
light_0_key = COT_Signal('17733', token)
temp_0_key = COT_Signal('2615', token)
humid_0_key = COT_Signal('10571', token)


# Plant 1 keys
soil_1_key = COT_Signal("28439", token)
pump_1_key = COT_Signal('20416', token)
light_1_key = COT_Signal('', token)
temp_1_key = COT_Signal('', token)
humid_1_key = COT_Signal('', token)


# Plant 2 keys
soil_2_key = COT_Signal('', token)
pump_2_key = COT_Signal('', token)
light_2_key = COT_Signal('', token)
temp_2_key = COT_Signal('', token)
humid_2_key = COT_Signal('', token)


# Plant 3 keys
soil_3_key = COT_Signal('', token)
pump_3_key = COT_Signal('', token)
light_3_key = COT_Signal('', token)
temp_3_key = COT_Signal('', token)
humid_3_key = COT_Signal('', token)


# Plant 4 keys
soil_4_key = COT_Signal('', token)
pump_4_key = COT_Signal('', token)
light_4_key = COT_Signal('', token)
temp_4_key = COT_Signal('', token)
humid_4_key = COT_Signal('', token)


# Plant 5 keys
soil_5_key = COT_Signal('', token)
pump_5_key = COT_Signal('', token)
light_5_key = COT_Signal('', token)
temp_5_key = COT_Signal('', token)
humid_5_key = COT_Signal('', token)


# Plant 6 keys
soil_6_key = COT_Signal('', token)
pump_6_key = COT_Signal('', token)
light_6_key = COT_Signal('', token)
temp_6_key = COT_Signal('', token)
humid_6_key = COT_Signal('', token)


# Plant 7 keys
soil_7_key = COT_Signal('', token)
pump_7_key = COT_Signal('', token)
light_7_key = COT_Signal('', token)
temp_7_key = COT_Signal('', token)
humid_7_key = COT_Signal('', token)


#### Plant signal arrays ####-------------------------------------------------------------------------------------------

"""
The arrangment of the sensor value posision in array:
plant name + 1 > 10^18  (1-8)
10^15 < soil_value < 10^18  (0-100)
10^9 < lux_value < 10^15 (0-999999)
10^6 < temp_value < 10^9 (0-100)
10^3 < humid_value < 10^6 (0-100)
water_level < 10^3 (0-100)

Example of plant 0 with all values maxed out: 1100999999100100100
"""

# Plant 0
plant_sensor_array_list = [COT_Signal('27693', token).get()['Value'], 2_007_000008_009_010_011]
plant_0 = COT_Signal('27693', token)

# Plant 1
plant_0_sensor_array = 1_000_000000_000_000_000

# Plant 2


# Plant 3


# Plant 4


# Plant 5


# Plant 6


# Plant 7





if __name__ == "__main__":
    plant_status = encode_plant_status('0')
    print(plant_status)
