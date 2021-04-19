# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 19:13:04 2021

@author: si_ve
"""

import requests
import json


#### CoT signal key ####
class COT_Signal:
    def __init__(self, key, token):
        self.key = key
        self.token = token
        self.payload = {"Key":self.key, "Token":self.token}

    def get(self):
        response = requests.get("https://circusofthings.com/ReadValue",
                                params = self.payload)
        response = json.loads(response.content)
        return response

    def put(self, value):
        self.value = value
        self.payload["Value"] = value
        response = requests.put("https://circusofthings.com/WriteValue",
                                params = self.payload,
                                data = json.dumps(self.payload),
                                headers = {"Content-Type":"application/json"})




#### Signal keys and token ####

token = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1Nzk0In0.nqXSqXGe2AXcNm4tdMUl7qIzmpAEXwr7UPKf5AtYx4k"

#### Plant 0 keys ####
soil_0_key = COT_Signal("4991", token)
pump_0_key = COT_Signal('32607', token)
light_0_key = COT_Signal('17733', token)
temp_0_key = COT_Signal('2615', token)
humid_0_key = COT_Signal('10571', token)


#### Plant 1 keys ####
soil_1_key = COT_Signal('', token)
pump_1_key = COT_Signal('20416', token)
light_1_key = COT_Signal('', token)
temp_1_key = COT_Signal('', token)
humid_1_key = COT_Signal('', token)


#### Plant 2 keys ####
soil_2_key = COT_Signal('', token)
pump_2_key = COT_Signal('', token)
light_2_key = COT_Signal('', token)
temp_2_key = COT_Signal('', token)
humid_2_key = COT_Signal('', token)


#### Plant 3 keys ####
soil_3_key = COT_Signal('', token)
pump_3_key = COT_Signal('', token)
light_3_key = COT_Signal('', token)
temp_3_key = COT_Signal('', token)
humid_3_key = COT_Signal('', token)


#### Plant 4 keys ####
soil_4_key = COT_Signal('', token)
pump_4_key = COT_Signal('', token)
light_4_key = COT_Signal('', token)
temp_4_key = COT_Signal('', token)
humid_4_key = COT_Signal('', token)


#### Plant 5 keys ####
soil_5_key = COT_Signal('', token)
pump_5_key = COT_Signal('', token)
light_5_key = COT_Signal('', token)
temp_5_key = COT_Signal('', token)
humid_5_key = COT_Signal('', token)


#### Plant 6 keys ####
soil_6_key = COT_Signal('', token)
pump_6_key = COT_Signal('', token)
light_6_key = COT_Signal('', token)
temp_6_key = COT_Signal('', token)
humid_6_key = COT_Signal('', token)


#### Plant 7 keys ####
soil_7_key = COT_Signal('', token)
pump_7_key = COT_Signal('', token)
light_7_key = COT_Signal('', token)
temp_7_key = COT_Signal('', token)
humid_7_key = COT_Signal('', token)
