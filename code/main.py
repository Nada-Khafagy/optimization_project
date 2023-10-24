import initialization
import objective_func
import platoon
import randomize_sequence
import Simulation
#import Whole_Systme
#global variables
alpha = 10
beta = 20
gamma = 20
merging_position = 150
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

(main_cars,ramp_cars) = initialization.initalize_cars(0,initial_main_velocity,initial_main_accelration,
                                                      0,initial_ramp_velocity,initial_ramp_accelration,
                                                      cars_main_line_no,cars_ramp_no)

#assume solution 
current_sequence = randomize_sequence.randomize()
sequence_full_info = dict()

for i in current_sequence:
    if i in main_cars:
        sequence_full_info[i] = main_cars[i]
    elif i in ramp_cars :
        sequence_full_info[i] = ramp_cars[i]
 

Simulation.platooning(main_cars,ramp_cars,sequence_full_info)
#platoon.platooning(main_cars)
w1 = 0.2
r = 5
rl = 1

