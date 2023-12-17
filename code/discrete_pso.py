from particle_class import Particle
import numpy as np
import math
from copy import copy
import sequence
import objective_func
import population

def discrete_pso( solution_size, var_min, var_max, Neighborhood_size, max_iter, inertia_w, c1, c2, synchronous,
        w_min, vel_min, vel_max,
                            star_topology, varying_w, weight_func_1, cc_parameters, road, main_cars_list, ramp_cars_list):
    
    # Create a population of particles with feasible positions:
    initial_population = population.initialize_population(Neighborhood_size, solution_size, main_cars_list, ramp_cars_list,road, cc_parameters)

    particles = [Particle(position) for position in initial_population]

    #caluclate initial fitness 
    initial_fitness = population.calc_fitness_list(particles, weight_func_1, main_cars_list, ramp_cars_list, cc_parameters, road)
    for fit, particle in zip(initial_fitness, particles):
        particle.fitness = fit
    
    population.update__global_best(particles, synchronous, star_topology)

    #used_for_data
    best_fitness_overall = None
    best_position_overall = None

    #used_for plotting
    best_particle_fitness_list = []
    best_particle_position_list = []
    

    w_initial = inertia_w
    for itr in range(max_iter):
        #update motion in which it updates personal best
        population.update_motion(particles, inertia_w, c1, c2, vel_min, vel_max, weight_func_1, cc_parameters, road, main_cars_list, ramp_cars_list)

        #update best
        [global_best_particle_fitness, global_best_particle_position] = population.update__global_best(particles)

        if global_best_particle_fitness > best_fitness_overall:
            best_fitness_overall = global_best_particle_fitness
            best_position_overall = global_best_particle_position
        

        best_particle_position_list.append(global_best_particle_position)
        best_particle_fitness_list.append(global_best_particle_fitness)

        #update inertia weight
        if varying_w :
            inertia_w = w_initial - itr * ((w_initial - w_min) / max_iter) 
        
        return best_particle_fitness_list, best_particle_position_list, best_fitness_overall,best_position_overall