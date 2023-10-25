import numpy as np
import objective_func
import randomize_sequence
import math
import Simulation
import initialization
import merged_platoon
import matplotlib.pyplot as plt

SA_temprature_List = []
SA_obj_func_List = []

def simulated_annealing(delta_time, decision_position,initial_main_v,initial_main_a,initial_ramp_v,initial_ramp_a,cars_main_line_no, merging_position,
                        cars_ramp_no, merged_sequence_size ,  initial_temperature, final_temperature, cooling_rate, num_iterations,
                          min_v,max_v,min_a,max_a,min_v_ramp,max_v_ramp,min_a_ramp,max_a_ramp, linear,w1, r_total,distances_to_merge):
    while (1):
        feasibility = True 
        #intialize a solution (list of sequences)
        [car_sequence, merged_ramp_size] = randomize_sequence.randomize(merged_sequence_size) 

        #map this sequence to cars' info in order to platoon
        car_sequence_info = dict()
        (main_cars,ramp_cars) = initialization.initalize_cars(decision_position,initial_main_v,initial_main_a,
                                                        decision_position-10,initial_ramp_v,initial_ramp_a,
                                                        cars_main_line_no,cars_ramp_no)
        for i in car_sequence:
            if i in main_cars:
                car_sequence_info[i] = main_cars[i]
            elif i in ramp_cars :
                car_sequence_info[i] = ramp_cars[i]

        while(list(car_sequence_info.values())[merged_sequence_size - 1].position < merging_position) and feasibility :    
            merged_platoon.platooning(car_sequence_info, delta_time)
            for car in list(car_sequence_info.values()):
                if car.name >=chr(97):
                    if not car.check_feasibility(min_v, max_v, min_a, max_a):
                        feasibility  = False
                        break       
                else:
                    if not car.check_feasibility(min_v_ramp, max_v_ramp, min_a_ramp, max_a_ramp):
                        feasibility  = False
                        break
             
        print("stuck1")
        print(car_sequence)
        #to debug
        if  True:
            print("not stuck") 
            break
            
    print("out1") 

    current_objective = objective_func.objective_func(w1, r_total,merged_ramp_size, car_sequence_info,distances_to_merge, min_v,max_v)
    print(r_total,merged_ramp_size)
    current_solution = car_sequence
    best_solution = current_solution
    best_objective = current_objective
    temperature = initial_temperature

    #SA algorithm
    for iteration in range(num_iterations):
        while (1):
            feasibility = True
            #intialize a solution (list of sequences)
            [car_sequence, merged_ramp_size] = randomize_sequence.randomize(merged_sequence_size) 

            #map this sequence to cars' info in order to platoon
            car_sequence_info = dict()
            (main_cars,ramp_cars) = initialization.initalize_cars(decision_position,initial_main_v,initial_main_a,
                                                            decision_position-10,initial_ramp_v,initial_ramp_a,
                                                            cars_main_line_no,cars_ramp_no)
            for i in car_sequence:
                if i in main_cars:
                    car_sequence_info[i] = main_cars[i]
                elif i in ramp_cars :
                    car_sequence_info[i] = ramp_cars[i]

            while(list(car_sequence_info.values())[merged_sequence_size - 1].position < merging_position) :    
                merged_platoon.platooning(car_sequence_info, delta_time)
                for car in list(car_sequence_info.values()):
                    if car.name >= chr(97):
                        if not car.check_feasibility(min_v, max_v, min_a, max_a):
                            feasibility  = False
                            break       
                    else:
                        if not car.check_feasibility(min_v_ramp, max_v_ramp, min_a_ramp, max_a_ramp):
                            feasibility  = False
                            break  
            print("stuck2")                  
            if True:
                break
        print( car_sequence )
        print(car.traveled_time for car in car_sequence_info.values() )
        new_objective = objective_func.objective_func(w1, r_total,merged_ramp_size, car_sequence_info,distances_to_merge, min_v,max_v)
        delta_objective = new_objective - current_objective
        
        if delta_objective > 0:
            current_solution = car_sequence
            current_objective = new_objective
            if current_objective >  best_objective:
                best_solution = current_solution
                best_objective = current_objective
        else :
            acceptance_prob = ((math.e)**(-1 * delta_objective)) / temperature 
            
            if acceptance_prob > np.random.rand():
                current_solution = car_sequence
                current_objective = new_objective

        SA_temprature_List.append(temperature)
        SA_obj_func_List.append(current_objective)

        if linear :
                
            temperature = initial_temperature - cooling_rate*iteration
        else :
            temperature = initial_temperature * cooling_rate

        print(temperature)
        if temperature <= final_temperature:
            break
                    


    return best_solution, best_objective , SA_temprature_List, SA_obj_func_List

