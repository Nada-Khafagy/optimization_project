import numpy as np
import objective_func
import math
import matplotlib.pyplot as plt


def simulated_annealing(iteration_index,current_solution,current_objective,
                        initial_temperature,curr_temperature,cooling_rate,linear,num_iterations,
                        min_v_main,max_v_main,
                        weight_func_1, cars_ramp_no,cars_ramp_merged_no,new_solution_dic,distances_to_merge):
    
    for _ in range(num_iterations):
        #fn+1
        new_objective = objective_func.objective_func(weight_func_1, cars_ramp_no,cars_ramp_merged_no,new_solution_dic,distances_to_merge, min_v_main,max_v_main)
        #delta f
        delta_objective = new_objective - current_objective

        if delta_objective >= 0: #we are maximizing so if it is positive, it is a good thing
            current_solution = new_solution_dic
            current_objective = new_objective
        else :
            #p 
            k = 1 # multiply by delta objective to make probability change greater 
            acceptance_prob = (math.e)** (((k*delta_objective)) / curr_temperature )
            print("probability is ",acceptance_prob)
            r =  np.random.rand()
            print("r is",r)
            if acceptance_prob > r:
                current_solution = new_solution_dic
                current_objective = new_objective    
    #apply cooling schedule
    if linear :          
        curr_temperature = initial_temperature - cooling_rate*iteration_index
    else :
        curr_temperature = initial_temperature * (cooling_rate**iteration_index)


     

    return current_solution, current_objective, curr_temperature



                
    
    