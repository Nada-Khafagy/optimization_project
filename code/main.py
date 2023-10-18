import intialize
import objective_func
#global variables
alpha = 0.2
beta = 0.5
gamma = 0.6
merging_position = 20
min_v = 60 * (5/18) #m/s
max_v = 120 * (5/18) #m/s


#initalize cars info
(main_cars,ramp_cars) = intialize.initalize_cars()

#assume solution 
current_sequence = ['A','a','b','B','C','c','D','E','F','G','H','I','J']
sequence_full_info = dict()

for i in current_sequence:
    if i in main_cars:
        sequence_full_info[i] = main_cars[i]
    elif i in ramp_cars :
        sequence_full_info[i] = ramp_cars[i]

intialize.platooning(sequence_full_info)

w1 = 0.2 #weight on maxmizing number pf cars joined , other weight is on minimizing time and is calculated w2=(1-w1)
r = 5 #total number of cars on ramp
rl = 2 #number of cars on ramp left (didn't merge)
print(objective_func.objective_func(w1, r, rl, sequence_full_info, min_v,max_v))