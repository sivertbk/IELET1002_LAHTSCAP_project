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
pump_1_key = COT_Signal('20416', token)
