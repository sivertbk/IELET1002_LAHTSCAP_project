import json

with open('data2.json') as json_file:
    dictionary = json.load(json_file)
    
dictionary["plant1"]["Config1"] = 11
dictionary["plant1"]["Config3"] = 3

with open('data2.json','w') as json_file:
    json.dump(dictionary, json_file)