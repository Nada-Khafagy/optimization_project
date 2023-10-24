import intialize
import objective_func
import SA

#import Whole_Systme
#global variables
alpha = 10
beta = 20
gamma = 20
merging_position = 20
min_v = 60 * (5/18) #m/s
max_v = 120 * (5/18) #m/s


#initalize cars info
(main_cars,ramp_cars) = intialize.initalize_cars()
test=dict()
#assume solution 
current_sequence = ['A','a','b','B','C','c','D','E','F','G','H','I','J']
sequence_full_info = dict()

for i in current_sequence:
    if i in main_cars:
        sequence_full_info[i] = main_cars[i]
    elif i in ramp_cars :
        sequence_full_info[i] = ramp_cars[i]
 

test['A'] = main_cars['A']
test['B'] = main_cars['B']
<<<<<<< HEAD

intialize.platooning(main_cars,ramp_cars,sequence_full_info)
#platoon.platooning(main_cars)

=======

intialize.platooning(main_cars,ramp_cars,sequence_full_info)
#platoon.platooning(main_cars)
>>>>>>> 6fa424ec66a8ab22c6c83768a0eae8a70d2059b1
w1 = 0.2
r = 5
rl = 1
SA.simulated_annealing()
#print(sequence_full_info)
#print(objective_func.objective_func(w1, r, rl, sequence_full_info, min_v,max_v))