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
delta_objective=0
current_objective=0

def simulated_annealing(num_iterations,first_iteration,
                        initial_temperature, final_temperature, cooling_rate,linear,
                        min_v,max_v,
                        w1, cars_ramp_no,cars_ramp_merged_no,new_solution_dic,distances_to_merge):
    global current_objective, current_solution
    flag_finish=False
    if(first_iteration):
        current_objective=0
        current_solution=None
    new_objective = objective_func.objective_func(w1, cars_ramp_no,cars_ramp_merged_no,new_solution_dic,distances_to_merge, min_v,max_v)
    delta_objective = new_objective - current_objective
    if linear :
            
        temperature = initial_temperature - cooling_rate*num_iterations
    else :
        temperature = initial_temperature * cooling_rate
    
    #print(temperature)
    if temperature <= final_temperature:
         flag_finish =True   
    if delta_objective > 0:
        current_solution = new_solution_dic
        current_objective = new_objective
    else :
        acceptance_prob = ((math.e)**(-1 * delta_objective)) / temperature 
        
        if acceptance_prob > np.random.rand():
            current_solution = new_solution_dic
            current_objective = new_objective

    
    
    
                    
    SA_temprature_List.append(temperature)
    SA_obj_func_List.append(current_objective)

    return current_solution, current_objective, flag_finish



                
    
    