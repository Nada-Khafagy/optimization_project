import vehicle_class
import random

def create_cars(initial_main_p,initial_main_v,initial_main_a,initial_ramp_p,initial_ramp_v,initial_ramp_a,cars_main_no,cars_ramp_no,random_pos_lower,random_pos_upper):

    #initalize cars on main line
    main_cars = dict() #dict of main cars object
    for i in range(cars_main_no):
        name = chr(65+i) # starts from A
        if i == 0:
            position = initial_main_p #starts with 0
        else:
            position = main_cars[chr(65+i-1)].position - 6 #distance to lead
        velocity = initial_main_v
        accelration = initial_main_a      
        car = vehicle_class.Vehicle(name, position, velocity, accelration)
        main_cars[name]= car

    #initalize cars on ramp
    ramp_cars = dict() #dict of ramp cars object
    for i in range(cars_ramp_no):
        name = chr(97+i) # starts from a
        if i == 0:
            position = initial_ramp_p #starts with 0
        else:
            position = ramp_cars[chr(97+i-1)].position - round(random.uniform(random_pos_lower, random_pos_upper))
        velocity = initial_ramp_v
        accelration = initial_ramp_a        
        car = vehicle_class.Vehicle(name, position, velocity, accelration)
        ramp_cars[name]=(car)

    return (main_cars,ramp_cars)


