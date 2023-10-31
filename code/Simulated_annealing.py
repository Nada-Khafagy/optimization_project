import random
import objective_func
import math
import matplotlib.pyplot as plt


def simulated_annealing(iteration_index,current_solution,current_objective,
                        initial_temperature,final_temperature,cooling_rate,linear,
                        min_v_main,max_v_main,
                        weight_func_1, cars_ramp_no,cars_ramp_merged_no,new_solution_dic,distances_to_merge):

    new_objective = objective_func.objective_func(weight_func_1, cars_ramp_no,cars_ramp_merged_no,new_solution_dic,distances_to_merge, min_v_main,max_v_main)
    delta_objective = new_objective - current_objective

    if linear :          
        curr_temperature = initial_temperature - cooling_rate*iteration_index
    else :
        curr_temperature = initial_temperature * (cooling_rate**iteration_index)

    #if it became zero or negative stop, why not leave it to return at ent of code? cuz might cause divide by zero
    if curr_temperature < final_temperature :
        return current_solution, current_objective, curr_temperature

    if delta_objective > 0: #we are maximizing so if it is positive, it is a good thing
        current_solution = new_solution_dic
        current_objective = new_objective
    else :
        acceptance_prob = (math.e)**(((-1 * delta_objective)) / curr_temperature )
        
        if acceptance_prob > random.randint(0,1):
            current_solution = new_solution_dic
            current_objective = new_objective


     

    return current_solution, current_objective, curr_temperature



                
    
    