# @Date:   2021-04-21T16:31:52+02:00
# @Last modified time: 2021-04-25T19:13:54+02:00

import requests
import json
import time


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

def encode_plant_input_status(plant_name):
    """
    This function takes a plant's inputs and arranges it to an array ready to be sent to CoT.
    First number in return value represents plant number so the value always stays the same length.
    """
    array = [int(plant_name)]
    # get statuses and store value in array
    array.append(plant_dictionary[str(plant_name)]['water'])
    array.append(plant_dictionary[str(plant_name)]['light'])
    array.append(plant_dictionary[str(plant_name)]['temp_state'])
    array.append(plant_dictionary[str(plant_name)]['humid_state'])
    array.append(plant_dictionary[str(plant_name)]['water_level_state'])

    # make array into a value to be sent
    for i in range(0,len(array)):
        status_value += str(array[i])
    return int(status_value)


def decode_plant_input_status(plant_name, input = 'default'):
    """
    This function takes a plant's input states as an array an decodes it to a dictionary of inputs and its state.
    Second argument takes plant input as keyword and returns state for given plant input. If second argument is ignored,
    return plants whole dictionary with all input states.
    """
    # get input state array for plant
    plant_state_array = int(plant_input_array_list[int(plant_name)-1].get()['Value'])
    # separate digits in input state array into list as string
    input_state_list = [str(i) for i in str(plant_state_array)]
    # arrange all the digits in correct posision in dictionary and convert into integers again.
    input_state_dict = {'plant':int(input_state_list[0]),
                        'pump':int("".join(input_state_list[1])),
                        'light':int("".join(input_state_list[2])),
                        'temp':int("".join(input_state_list[3])),
                        'humid':int("".join(input_state_list[4])),
                        'water_level':int("".join(input_state_list[5]))
                        }
    # return whole dictionary if second argument is not given
    if input == 'default':
        return input_state_dict
    else:
        return sensor_values_dict[input]



def decode_sensor_values(plant_name, sensor = 'default'):
    """
    This function takes a plant's outputs (sensor values) as an array an decodes it to a dictionary of sensor values.
    Second argument takes sensor as keyword and returns value for given sensor. If second argument is ignored, return
    plants whole dictionary with all sensor values.
    """

    # get sensor value array for plant
    plant_sensor_array = int(plant_sensor_array_list[int(plant_name)-1].get()['Value'])
    # separate digits in sensor value array into list as string
    sensor_values_list = [str(i) for i in str(plant_sensor_array)]
    # arrange all the digits in correct posision in dictionary and convert into integers again.
    sensor_values_dict = {'plant':int(sensor_values_list[0]),
                          'soil':int("".join(sensor_values_list[1:4])),
                          'lux':int("".join(sensor_values_list[4:10])),
                          'temp':int("".join(sensor_values_list[10:13])),
                          'humid':int("".join(sensor_values_list[13:16])),
                          'water_level':int("".join(sensor_values_list[16:]))
                          }
    # return whole dictionary if second argument is not given
    if sensor == 'default':
        return sensor_values_dict
    else:
        return sensor_values_dict[sensor]



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


#### Plant sensor signal arrays ####------------------------------------------------------------------------------------

"""
The arrangment of the sensor value posision in array:

plant name > 10^18             range: (1-8)
10^15 < soil_value < 10^18     range: (0-100)
10^9 < lux_value < 10^15       range: (0-999999)
10^6 < temp_value < 10^9       range: (0-100)
10^3 < humid_value < 10^6      range: (0-100)
water_level < 10^3             range: (0-100)

Example of plant 1 with all values maxed out: 1100999999100100100
"""

# Plant 1
plant_1_sensor_key = '27693'
# Plant 2
plant_2_sensor_key = '13508'
# Plant 3
plant_3_sensor_key = '6796'
# Plant 4
plant_4_sensor_key = ''
# Plant 5
plant_5_sensor_key = ''
# Plant 6
plant_6_sensor_key = ''
# Plant 7
plant_7_sensor_key = ''
# Plant 8
plant_8_sensor_key = ''

plant_sensor_array_list = [COT_Signal(plant_1_sensor_key, token),  # Plant 1
                           COT_Signal(plant_2_sensor_key, token),  # Plant 2
                           COT_Signal(plant_3_sensor_key, token),  # Plant 3
                           COT_Signal(plant_4_sensor_key, token),  # Plant 4
                           COT_Signal(plant_5_sensor_key, token),  # Plant 5
                           COT_Signal(plant_6_sensor_key, token),  # Plant 6
                           COT_Signal(plant_7_sensor_key, token),  # Plant 7
                           COT_Signal(plant_8_sensor_key, token)   # Plant 8
                           ]

#### Plant sensor signal arrays ####------------------------------------------------------------------------------------

"""
The arrangment of the inputs posision in array:

plant name > 10^4
10^3 < pump_state < 10^4
10^2 < light_state < 10^3
10^1 < temp_state < 10^2
10^0 < humid_state < 10^1
water_tank_state < 10^0

Example of plant 1 with random states: 101220
"""

# Plant 1
plant_1_input_key = '23560'
# Plant 2
plant_2_input_key = '31609'
# Plant 3
plant_3_input_key = '1005'
# Plant 4
plant_4_input_key = ''
# Plant 5
plant_5_input_key = ''
# Plant 6
plant_6_input_key = ''
# Plant 7
plant_7_input_key = ''
# Plant 8
plant_8_input_key = ''

plant_input_array_list = [COT_Signal(plant_1_input_key, token),  # Plant 1
                          COT_Signal(plant_2_input_key, token),  # Plant 2
                          COT_Signal(plant_3_input_key, token),  # Plant 3
                          COT_Signal(plant_4_input_key, token),  # Plant 4
                          COT_Signal(plant_5_input_key, token),  # Plant 5
                          COT_Signal(plant_6_input_key, token),  # Plant 6
                          COT_Signal(plant_7_input_key, token),  # Plant 7
                          COT_Signal(plant_8_input_key, token)   # Plant 8
                          ]



if __name__ == "__main__":
    while True:
        signal = decode_sensor_values(1)
        print(signal)
        time.sleep(1)
