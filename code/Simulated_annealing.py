import numpy as np
from objective_func import fitness
import math
import matplotlib.pyplot as plt
from sequence import randomize_sequence
from sequence import get_car_object_list_from_sequence
from sequence import get_distance_to_merge_list
from sequence import check_feasibility
from sequence import turn_binary_to_letters
from sequence import turn_letters_to_binary
from sequence import get_sequence_in_letters_from_cars



def simulated_annealing(initial_temperature,
final_temperature,num_iterations,iteration_per_temp, cooling_rate,linear, main_cars_list, ramp_cars_list,solution_size, weight_func_1,
 road, cc_parameters, plot_best):   
    current_solution = None
    current_fitness = 0
    best_solution = None
    best_fitness = 0
    iteration_index = 0
    #travel_time=[]
    SA_temprature_List = []
    SA_fitness_List = []
    curr_temperature = initial_temperature

    while(curr_temperature > final_temperature) and (curr_temperature>0) and (iteration_index<num_iterations):
        for _ in range(iteration_per_temp):
            #generate new solution
            [new_solution, ramp_merged_num]= randomize_sequence(solution_size, len(ramp_cars_list))  
            #get objects from the randomized list
            [new_solution_obj, distances_to_merge_list] = get_car_object_list_from_sequence(new_solution, main_cars_list, ramp_cars_list, cc_parameters)
            #check feasibility
            if (not check_feasibility(new_solution_obj, road, cc_parameters)):
                #don't count this iteration and get another solution
                continue
            #get the list of distances, which is needed when getting the fitness

            #fn+1
            new_fitness = fitness(weight_func_1, len(ramp_cars_list), ramp_merged_num,new_solution_obj,distances_to_merge_list, road)
            #delta f
            delta_fitness = new_fitness - current_fitness
            if delta_fitness >= 0: #we are maximizing so if it is positive, it is a good thing
                current_solution = new_solution_obj
                current_fitness = new_fitness
            else :
                #p 
                k = 50 # multiply by delta fitness to make probability change greater 
                acceptance_prob = (math.e)** ((k*delta_fitness) / curr_temperature )
                random_num =  np.random.rand()
                if acceptance_prob > random_num:
                    current_solution = new_solution_obj
                    current_fitness = new_fitness 
            
            #update best solution and fitness
            if (best_solution is None) or (best_fitness < current_fitness) :
                best_solution = current_solution
                best_fitness = current_fitness   

            #apply cooling schedule
            if linear :          
                curr_temperature = initial_temperature - cooling_rate*iteration_index
            else :
                curr_temperature = initial_temperature * (cooling_rate**iteration_index)

            #collect data to plot
            SA_temprature_List.append(curr_temperature) #x-axsis
            if plot_best :
                SA_fitness_List.append(best_fitness)
            else:
                SA_fitness_List.append(current_solution)

            
            #return cars to initial conditions
            for car in current_solution:
                car.return_to_initial_conditions()

            iteration_index += 1
                 
            print("Accepted Sequence is: ", get_sequence_in_letters_from_cars(current_solution))
            print("current fitness:", current_fitness)
          
    return best_solution, best_fitness, SA_temprature_List, SA_fitness_List



                
    
    