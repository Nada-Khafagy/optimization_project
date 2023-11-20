import vehicle_class
import random

def create_cars(vehicle_generation_parameters):
    #initalize cars 
    car_list = list() #dict of main cars object
    for i in range(vehicle_generation_parameters.vehicles_num):
        if (vehicle_generation_parameters.lane_num == 1):
            name = chr(65+i) # starts from A
        else:
            name = chr(97+i) # starts from a
        if i == 0:
            position =  vehicle_generation_parameters.initial_position #starts with 0
        else:
            position = car_list[i-1].position - round(random.uniform(vehicle_generation_parameters.road.position_lower_limit, 
                                                                     vehicle_generation_parameters.road.position_upper_limit)) #distance to lead           
        velocity = vehicle_generation_parameters.initial_velocity
        accelration = vehicle_generation_parameters.initial_acceleration  
        new_car = vehicle_class.Vehicle(name, position, velocity, accelration)
        car_list.append(new_car)

    return car_list


