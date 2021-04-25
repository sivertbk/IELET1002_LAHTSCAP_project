# @Date:   2021-04-21T16:31:52+02:00
# @Last modified time: 2021-04-21T17:39:29+02:00

import requests
import json


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
active_status_key2 = COT_Signal('3904', token)

#### Plant sensor and output signal keys ####---------------------------------------------------------------------------

# Plant 0 keys
soil_0_key = COT_Signal("4991", token)
pump_0_key = COT_Signal('32607', token)
light_0_key = COT_Signal('17733', token)
temp_0_key = COT_Signal('2615', token)
humid_0_key = COT_Signal('10571', token)
ultrasonic_0_key = COT_Signal('28799', token)


# Plant 1 keys
soil_1_key = COT_Signal("28439", token)
pump_1_key = COT_Signal('20416', token)
light_1_key = COT_Signal('', token)
temp_1_key = COT_Signal('', token)
humid_1_key = COT_Signal('', token)
ultrasonic_1_key = COT_Signal('', token)


# Plant 2 keys
soil_2_key = COT_Signal('', token)
pump_2_key = COT_Signal('', token)
light_2_key = COT_Signal('', token)
temp_2_key = COT_Signal('', token)
humid_2_key = COT_Signal('', token)
ultrasonic_2_key = COT_Signal('', token)

# Plant 3 keys
soil_3_key = COT_Signal('', token)
pump_3_key = COT_Signal('', token)
light_3_key = COT_Signal('', token)
temp_3_key = COT_Signal('', token)
humid_3_key = COT_Signal('', token)
ultrasonic_3_key = COT_Signal('', token)

# Plant 4 keys
soil_4_key = COT_Signal('', token)
pump_4_key = COT_Signal('', token)
light_4_key = COT_Signal('', token)
temp_4_key = COT_Signal('', token)
humid_4_key = COT_Signal('', token)
ultrasonic_4_key = COT_Signal('', token)

# Plant 5 keys
soil_5_key = COT_Signal('', token)
pump_5_key = COT_Signal('', token)
light_5_key = COT_Signal('', token)
temp_5_key = COT_Signal('', token)
humid_5_key = COT_Signal('', token)
ultrasonic_5_key = COT_Signal('', token)

# Plant 6 keys
soil_6_key = COT_Signal('', token)
pump_6_key = COT_Signal('', token)
light_6_key = COT_Signal('', token)
temp_6_key = COT_Signal('', token)
humid_6_key = COT_Signal('', token)
ultrasonic_6_key = COT_Signal('', token)

# Plant 7 keys
soil_7_key = COT_Signal('', token)
pump_7_key = COT_Signal('', token)
light_7_key = COT_Signal('', token)
temp_7_key = COT_Signal('', token)
humid_7_key = COT_Signal('', token)
ultrasonic_7_key = COT_Signal('', token)