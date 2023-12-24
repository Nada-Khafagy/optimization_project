from particle_class import Particle
import numpy as np
import math
from copy import copy
import sequence
import objective_func
import population

def discrete_pso(DPSO_parameters):
    solution_size, Neighborhood_size, max_iter, c1, c2, synchronous, vel_max, star_topology, weight_func_1, cc_parameters, road, main_cars_list, ramp_cars_list = DPSO_parameters[:]

    # Create a population of particles with feasible positions:
    initial_solutions = population.initialize_population(Neighborhood_size, solution_size, main_cars_list, ramp_cars_list,road, cc_parameters)
    particles = [Particle(solution) for solution in initial_solutions] #intalizes solution and position

    #caluclate initial fitness 
    initial_fitness = population.calc_fitness_list(initial_solutions, weight_func_1, main_cars_list, ramp_cars_list, cc_parameters, road)
    for fit, particle in zip(initial_fitness, particles):
        particle.fitness = fit

    #used for data analysis
    best_solution_overall = []
    best_fitness_overall = 0
    best_particle_fitness_list = []
    #best_particle_position_list = []
    
    for _ in range(max_iter):
        [global_best_particle_solution, global_best_particle_fitness] = population.update_global_best(particles, star_topology)
        for particle in particles:
            #update motion in which it updates personal best
            #check feasibilty is inside update_motion
            population.update_motion(particle, c1, c2, vel_max, weight_func_1, cc_parameters, road, main_cars_list, ramp_cars_list)
            if not synchronous :
                #update best
                [global_best_particle_solution, global_best_particle_fitness] = population.update_global_best(particles, star_topology)

            
            if global_best_particle_fitness > best_fitness_overall:
                best_fitness_overall = global_best_particle_fitness
                best_solution_overall = global_best_particle_solution
 
            #best_particle_position_list.append(global_best_particle_solution)
        best_particle_fitness_list.append(global_best_particle_fitness) 
        
    return range(max_iter), best_particle_fitness_list, best_solution_overall, best_fitness_overall