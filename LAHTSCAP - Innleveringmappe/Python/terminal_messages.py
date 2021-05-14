# @Date:   2021-04-26T14:08:42+02:00
# @Last modified time: 2021-04-29T15:10:56+02:00



'''
Functions that makes serial printing in main loop a little bit smoother and neat.
'''

import time
from datetime import datetime
import plant_modules


def plant_checktime_left(plant_name):
    '''
    function gives time left until watering if in soil control.
    '''
    
    current_time = int(time.time())
    soil_time_tracker = plant_modules.soil_time_tracker[str(plant_name)]
    control_wait_time = plant_modules.plant_soil_check_control_time

    print()

    time_left = (soil_time_tracker + control_wait_time) - current_time

    if plant_modules.soil_control[str(plant_name)] == False:
        message = ('Soil control time set to: '+ str(control_wait_time)+ ' seconds.')
        return message
    
    else:
        message = ('Activate pump in: '+ datetime.fromtimestamp(time_left).strftime('%M:%S'))        
        return message






if __name__ == "__main__":
    print(plant_checktime_left('1'))
