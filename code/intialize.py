import random
import matplotlib.pyplot as plt
import vehicle_class
import scatter_custom
#constraints
min_v = 60 * (5/18) #m/s
max_v = 120 * (5/18) #m/s
min_a = -6 #m/s^2
max_a = 5 #m/s^2
min_a_ramp = -3 #m/s^2
max_a_ramp = 3 #m/s^2

# intlizing parameters
cars_main_line_no = 10
cars_ramp_no = 5
initial_main_velocity = 60  * 5/18  #m/s
initial_main_accelration = 3 #m/s^2

initial_ramp_velocity = 55 * 5/18 #m/s
initial_ramp_accelration = 0 #m/s^2
initial_pos_upper = 7
initial_pos_lower = 5

#parameters to update kinematics
decision_position = 90 #m, position where we apply cruse control
merging_position = 20 #m, position of point of merging
delta_time = 0.01 #seconds, sampling time
desired_distance_bet_cars = 6#m
alpha = 1
beta = 1.2
gamma = 0.5

#cars on main line list
main_cars_platoon = dict() #list of car object
ramp_cars = dict() #i want to mak the main line a list as well but to edit that i have no time at the moment

#car labels
car_labels = []  # List to store car labels
car_labels_updates = [] 
#car average velocities
car_avg_velocities = []
car_labels_ramps=[]


def initalize_cars():

    for i in range(cars_main_line_no):
        name = chr(65+i) # starts from A
        if i == 0:
            position = 0 #starts with 0
        else:
            position = main_cars_platoon[chr(65+i-1)].position - round(random.uniform(initial_pos_lower, initial_pos_upper))

        velocity = initial_main_velocity
        accelration = initial_main_accelration
        
        car = vehicle_class.Vehicle(name, position, velocity, accelration)
        main_cars_platoon[name]= car


    #initalize cars on ramp
    for i in range(cars_ramp_no):
        name = chr(97+i) # starts from A
        if i == 0:
            position = 0 #starts with 0
        else:
            
            position = ramp_cars[chr(97+i-1)].position - round(random.uniform(initial_pos_lower, initial_pos_upper))

        #for making last cars on ramp solwer(cars which will not go onto main road)
        '''if i < 3:
            velocity = initial_ramp_velocity
        else:
            velocity = initial_ramp_velocity - 10
        velocity = initial_ramp_velocity'''

        accelration = initial_ramp_accelration
        
        car = vehicle_class.Vehicle(name, position, velocity, accelration)
        ramp_cars[name]=(car)

    return (main_cars_platoon,ramp_cars)




