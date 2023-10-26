import initialization
import objective_func
import platoon
import randomize_sequence
import Simulation
import SA
import merged_platoon
import matplotlib.pyplot as plt

#import Whole_Systme
#global variables
alpha = 10
beta = 20
gamma = 20
decision_position = 40#m, position where we apply cruse control
merging_position = 140 #m, position of point of merging
delta_time = 0.01 #seconds, sampling time

#constraints
min_v = 10 * (5/18) #m/s
max_v = 120 * (5/18) #m/s
min_v_ramp = 5 * (5/18) #m/s
max_v_ramp = 120 * (5/18) #m/s
min_a_ramp = -3 #m/s^2
max_a_ramp = 3 #m/s^2
min_a = -6 #m/s^2
max_a = 5 #m/s^2


#initalize cars info
# intlizing parameters
merged_sequence_size = 8
cars_main_line_no = 10
cars_ramp_no = 5
initial_main_velocity = 60  * 5/18  #m/s
initial_main_accelration = 3 #m/s^2

initial_ramp_velocity = 55 * 5/18 #m/s
initial_ramp_accelration = 0 #m/s^2


(main_cars,ramp_cars) = initialization.initalize_cars(decision_position,initial_main_velocity,initial_main_accelration,
                                                      decision_position-10,initial_ramp_velocity,initial_ramp_accelration,
                                                      cars_main_line_no,cars_ramp_no)

#assume solution 
r = cars_ramp_no 
current_sequence =['A', 'a', 'B', 'C', 'D', 'E', 'b', 'c']
sequence_full_info = dict()

for i in current_sequence:
    if i in main_cars:
        sequence_full_info[i] = main_cars[i]
    elif i in ramp_cars :
        sequence_full_info[i] = ramp_cars[i]
 
sequence_full_info_list = list(sequence_full_info.values())

#Simulation.platooning(main_cars,ramp_cars,sequence_full_info)


distances_to_merge = []

for i in range(merged_sequence_size):
    car = sequence_full_info_list[i]
    distances_to_merge.append(merging_position- car.position)

#print(distances_to_merge)

#cruise control 
while(sequence_full_info_list[merged_sequence_size-1].position < merging_position):    
    merged_platoon.platooning(sequence_full_info,delta_time)
    for car in list(sequence_full_info.values()):
        print(car.velocity, car.acceleration)


#Example usage
initial_temperature = 100.0
cooling_rate = 0.6
num_iterations = 100 
final_temperature = 5

w1 = 0.5
rl = 1
min_v = 60  * 5/18 #m/s
max_v = 120 * (5/18) #m/s
linear = True

#platoon.platooning(main_cars)
print(objective_func.objective_func(w1,cars_ramp_no,r,sequence_full_info,distances_to_merge,min_v,max_v))
