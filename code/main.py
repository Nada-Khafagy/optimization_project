import intialize

#global variables
alpha = 0.2
beta = 0.5
gamma = 0.6
distance_to_merging = 20


#get cars info
main_cars = intialize.get_main_cars_list()
ramp_cars = intialize.get_ramp_cars_list()

#assume solution 
current_sequence = ['A','a','b','B','C','c','D','E','F','d','G','H','I','J']
sequence_full_info = dict()

for i in current_sequence:
    if i in main_cars:
        sequence_full_info[i] = main_cars[i]
    elif i in ramp_cars :
        sequence_full_info[i] = ramp_cars[i]


intialize.platooning(sequence_full_info)
