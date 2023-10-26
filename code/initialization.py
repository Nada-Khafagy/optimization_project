import vehicle_class
import random

main_cars_platoon = dict() #dict of main cars object
ramp_cars = dict() #dict of ramp cars object
initial_pos_upper=8
initial_pos_lower=5

def initalize_cars(initial_main_p,initial_main_v,initial_main_a,initial_ramp_p,initial_ramp_v,initial_ramp_a,cars_main_line_no,cars_ramp_no):

    for i in range(cars_main_line_no):
        name = chr(65+i) # starts from A
        if i == 0:
            position = initial_main_p #starts with 0
        else:
            position = main_cars_platoon[chr(65+i-1)].position - 6 #distance to lead

        velocity = initial_main_v
        accelration = initial_main_a
        
        car = vehicle_class.Vehicle(name, position, velocity, accelration)
        main_cars_platoon[name]= car

    '''#print created main cars
    for c in main_cars_platoon.values():
        print(c)'''

    #initalize cars on ramp
    for i in range(cars_ramp_no):
        name = chr(97+i) # starts from A
        if i == 0:
            position = initial_ramp_p #starts with 0
        else:
            position = ramp_cars[chr(97+i-1)].position - 5#round(random.uniform(initial_pos_lower, initial_pos_upper))

        velocity = initial_ramp_v
        accelration = initial_ramp_a
        
        car = vehicle_class.Vehicle(name, position, velocity, accelration)
        ramp_cars[name]=(car)

    '''#print created ramp cars
    for c in ramp_cars:
        print(c)'''
    
    return (main_cars_platoon,ramp_cars)


