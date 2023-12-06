import random
from collections import deque
from cruise_control import cruise_control
class sequence:
    def __init__(self, sequence, main_cars_list, ramp_cars_list, road, cc_parameters):
        self.sequence = sequence
        self.main_cars_list = main_cars_list
        self.ramp_cars_list = ramp_cars_list
        self.road = road
        self.cc_parameters = cc_parameters


#returns list of sequence in binary format
def randomize_sequence(sequence_size, ramp_cars_max_num):
    sequence = [1] * sequence_size #create list of the final optimized seq. 
    ramp_cars_num = random.randint(1, ramp_cars_max_num) #randomize the number of added ramp cars to the final list 
    for _ in range(ramp_cars_num):
        while True:
            random_num = random.randint(0, sequence_size-1) # generte random --index-- to where we will put a ramp car 
            if sequence[random_num] == 1:
                sequence[random_num] = 0
                break  # Exit the inner loop
    return sequence

#works with binary 
def get_car_object_list_from_sequence(binary_sequece, main_cars_list, ramp_cars_list):

    vehicle_objects_sequence = list()
    main_cars_queue = deque(main_cars_list)
    ramp_cars_queue = deque(ramp_cars_list)
    for car_name in binary_sequece: 
        if car_name == 1:
            vehicle_objects_sequence.append(main_cars_queue.popleft())           
        else:
            vehicle_objects_sequence.append(ramp_cars_queue.popleft()) 
    return  vehicle_objects_sequence

#works only before crusie control, which is called in check feasability so works only before feasability check
def get_distance_to_merge_list(vehicle_objects_sequence, cc_parameters):
    distances_to_merge_list = []
    for car in vehicle_objects_sequence:    
        distances_to_merge_list.append(cc_parameters.merging_position - car.position)
    return distances_to_merge_list

#check constraints
#vehicle sequence is binary
def check_feasibility(vehicle_sequence, road, cc_parameters, main_cars_list, ramp_cars_list):
    curr_ramp_cars_num = len(vehicle_sequence) - sum(vehicle_sequence);     
    # check on number of ramp cars if solution has more ramp cars than actual scenario
    if curr_ramp_cars_num > len(ramp_cars_list):
        return False
    
    #get objects to simulate the dynamics
    vehicle_objects_sequence = get_car_object_list_from_sequence(vehicle_sequence, main_cars_list, ramp_cars_list)
    for car in vehicle_objects_sequence :
         car.return_to_initial_conditions()
    feasibility = True
    while(vehicle_objects_sequence[-1].position < cc_parameters.merging_position ): 
        #move all cars for one time sample 
        cruise_control(vehicle_objects_sequence, cc_parameters) 
        
        #chack if all cars follows road rules     
        for car in vehicle_objects_sequence:
            #if one car is not feasible, whole solution is not feasible
            #check if the car follows car rulse (velocity / accelration)
            if not car.follows_road_rules(road):
                return False    

    return feasibility


def turn_binary_to_letters(binary_sequence):
    index_main_car = 0 
    index_ramp_car = 0
    letter_sequence = []
    for num in binary_sequence:
        if num == 1:
            letter_sequence.append(chr(65+index_main_car))
            index_main_car+=1
        else:
            letter_sequence.append(chr(97+index_ramp_car))
            index_ramp_car+=1  
    return letter_sequence

def turn_letters_to_binary(letters_sequence):
    binary_sequence = [0 if letter >= chr(97) else 1 for letter in letters_sequence]
    return binary_sequence

def turn_car_objects_to_letters(sequence):
    letters_sequence = []
    for car in sequence:
        letters_sequence.append(car.name)
    return letters_sequence

def turn_car_objects_to_binary(sequence):
    binary_sequence = [0 if car.name >= chr(97) else 1 for car in sequence]
    return binary_sequence