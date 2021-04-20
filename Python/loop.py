# @Author: Sivert Berg Knudsen <sivertbk>
# @Date:   2021-04-15T16:16:12+02:00
# @Email:  si_vert@hotmail.com
# @Filename: loop.py
# @Last modified by:
# @Last modified time: 2021-04-20T23:17:56+02:00

from plant_status import *

if __name__ == "__main__":
    while True:

        #### Update sensor values ####----------------------------------------------------------------------------------
        for plant_name in range(0, 2):
            update_plant_soil_value(plant_name)
            update_plant_water_state(plant_name)

        #### Check sensors ####-----------------------------------------------------------------------------------------

            plant_soil_check(plant_name)

        #### Water and light ####---------------------------------------------------------------------------------------
            water(plant_name)


            #print(plant[str(plant_name)]['soil_value'])
            #print(datetime.fromtimestamp(plant[str(plant_name)]['last_water']).strftime('%Y-%m-%d %H:%M:%S'))





        print('##########################################################')
        print('PLANT STATUSES:')
        for plant_name in range(0, 2):
            print('\n  Plant', str(plant_name) +':')
            print('  Soil:', int(plant[str(plant_name)]['soil_value']), '    Threshold:', plant[str(plant_name)]['water_requirement'])
            print('  Pump:', plant[str(plant_name)]['water'], '  Last given water:', datetime.fromtimestamp(plant[str(plant_name)]['last_water']).strftime('%H:%M:%S %d/%m-%Y'))

        print('##########################################################')





        time.sleep(1)
