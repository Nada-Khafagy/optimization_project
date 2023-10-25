import initialization
import objective_func
import platoon
import randomize_sequence
import Simulation
import merged_platoon
#import Whole_Systme
#global variables
alpha = 10
beta = 20
gamma = 20
decision_position = 40#m, position where we apply cruse control
merging_position = 140 #m, position of point of merging
delta_time = 0.01 #seconds, sampling time
min_v = 60 * (5/18) #m/s
max_v = 120 * (5/18) #m/s


#initalize cars info
# intlizing parameters
cars_main_line_no = 10
cars_ramp_no = 5
initial_main_velocity = 60  * 5/18  #m/s
initial_main_accelration = 3 #m/s^2

initial_ramp_velocity = 55 * 5/18 #m/s
initial_ramp_accelration = 0 #m/s^2

(main_cars,ramp_cars) = initialization.initalize_cars(decision_position,initial_main_velocity,initial_main_accelration,
                                                      decision_position-20,initial_ramp_velocity,initial_ramp_accelration,
                                                      cars_main_line_no,cars_ramp_no)

#assume solution 
[current_sequence,r,m] = randomize_sequence.randomize()
sequence_full_info = dict()

for i in current_sequence:
    if i in main_cars:
        sequence_full_info[i] = main_cars[i]
    elif i in ramp_cars :
        sequence_full_info[i] = ramp_cars[i]
 
while(list(sequence_full_info.values())[7].position<merging_position):
    distances_to_merge = merged_platoon.platooning(sequence_full_info,delta_time)
#platoon.platooning(main_cars)

#print(distances_to_merge)
print(objective_func.objective_func(0.5,cars_ramp_no,r,sequence_full_info,distances_to_merge,min_v,max_v))


