import numpy as np
import objective_func
import randomize_sequence
import math
import Simulation
import initialization


def simulated_annealing(initial_main_p,initial_main_v,initial_main_a,initial_ramp_p,initial_ramp_v,initial_ramp_a,cars_main_line_no,
                        cars_ramp_no, initial_temperature, final_temperature, cooling_rate, num_iterations, w1,r,r1,min_v,max_v, linear):

    #intialize a solution (list of sequences)
    (_ ,car_sequence) = randomize_sequence.randomize() 

    #map this sequence to cars' info in order to platoon
    car_sequence_info = dict()
    (main_cars,ramp_cars) = initialization.initalize_cars(0,initial_main_v,initial_main_a,
                                                      0,initial_ramp_v,initial_ramp_a,
                                                      cars_main_line_no,cars_ramp_no)
    for i in car_sequence:
        if i in main_cars:
            car_sequence_info[i] = main_cars[i]
        elif i in ramp_cars :
            car_sequence_info[i] = ramp_cars[i]

    (feasibilty,_) = Simulation.platooning(main_cars,ramp_cars,car_sequence_info)

    current_objective = objective_func.objective_func(w1, r, r1, car_sequence_info, min_v,max_v)
    current_solution = car_sequence
    best_solution = current_solution
    best_objective = current_objective
    temperature = initial_temperature

    #SA algorithm
    for i in range(num_iterations):
        car_sequence = randomize_sequence.randomize() 
        car_sequence_info = dict()
        (main_cars,ramp_cars) = initialization.initalize_cars(0,initial_main_v,initial_main_a,
                                                      0,initial_ramp_v,initial_ramp_a,
                                                      cars_main_line_no,cars_ramp_no)
    for i in car_sequence:
        if i in main_cars:
            car_sequence_info[i] = main_cars[i]
        elif i in ramp_cars :
            car_sequence_info[i] = ramp_cars[i]
 

        

        new_objective = objective_func.objective_func( w1, r, r1, car_sequence_info, min_v, max_v)
        delta_objective = new_objective - current_objective
        
        if delta_objective < 0:
            current_solution = car_sequence
            current_objective = new_objective
            if current_objective < best_objective:
                best_solution = current_solution
                best_objective = current_objective
        else :
            acceptance_prob = ((math.e)^(-1 * delta_objective)) / temperature 
            
            if acceptance_prob > np.random.rand():
                current_solution = car_sequence
                current_objective = new_objective
            if linear :
                temperature = initial_temperature - cooling_rate*i
            else :
                temperature = initial_temperature * cooling_rate
        if temperature <= final_temperature:
            break
                

    return best_solution, best_objective

