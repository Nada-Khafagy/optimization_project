import numpy as np
from objective_func import fitness
import math
import matplotlib.pyplot as plt
import sequence




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
            new_solution = sequence.randomize_sequence(solution_size, len(ramp_cars_list))  
            #get objects from the randomized list
            new_solution_obj = sequence.get_car_object_list_from_sequence(new_solution, main_cars_list, ramp_cars_list)
            #check feasibility
            if (not sequence.check_feasibility(new_solution_obj, road, cc_parameters)):
                #don't count this iteration and get another solution
                continue
            #get the list of distances, which is needed when getting the fitness

            #fn+1
            new_fitness = fitness(weight_func_1, len(ramp_cars_list),new_solution_obj, cc_parameters, road)
            #delta f
            delta_fitness = new_fitness - current_fitness
            #print("delta_fitness",delta_fitness)
            if delta_fitness >= 0: #we are maximizing so if it is positive, it is a good thing
                current_solution = new_solution_obj
                current_fitness = new_fitness
            else :
                #p 
                k = 50 # multiply by delta fitness to make probability change greater 
                acceptance_prob = ((math.e)**(k*delta_fitness)) / curr_temperature 
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

            #print("curr_temperature",curr_temperature)
            #print("current SA solution:", sequence.turn_car_objects_to_binary(current_solution))
            #print("current SA fitness:", current_fitness)

            #collect data to plot
            SA_temprature_List.append(curr_temperature) #x-axsis
            if plot_best :
                SA_fitness_List.append(best_fitness)
            else:
                SA_fitness_List.append(current_fitness)

            
            #return cars to initial conditions
            for car in current_solution:
                car.return_to_initial_conditions()

            iteration_index += 1
                 
            #print("Accepted Sequence is: ", sequence.turn_car_objects_to_letters(current_solution))
            #print("current fitness:", current_fitness)
          
    return best_solution, best_fitness, SA_temprature_List, SA_fitness_List



                
    
    