import calibration as cal


"""
Trying to figure out how to deal with mulitple plants config and how to switch between them while using the same code.
"""
plant_dictionary = {"0":{}}
plant_dictionary["0"]["Temp"] = cal.temp
plant_dictionary["0"]["Soil"] = cal.soil
plant_dictionary["0"]["Humid"] = cal.humid
plant_dictionary["0"]["Pump"] = cal.pump

print(plant_dictionary)

plant_dictionary["1"] = {}
plant_dictionary["1"] = plant_dictionary["0"]

print(plant_dictionary)