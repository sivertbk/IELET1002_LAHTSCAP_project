import json

# Get the dictionary and store to variable
with open('data2.json') as json_file:
    dictionary = json.load(json_file)

"""
Read values, make changes to existing elements, store new elements
"""

print(dictionary)
    