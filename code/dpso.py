import particle_class
import numpy as np
import math
import copy
import sequence
import objective_func

def discrete_pso( solution_size, var_min, var_max, population_size, max_iter, c1, c2, vel_min, vel_max, w_max, w_min,
                 w1,cc_parameters, road, main_cars_list, ramp_cars_list):
    
    empty_particle = particle_class.particle(solution_size)

    # Create a population of empty particles:
    population = np.array([particle_class.particle(solution_size) for _ in range(population_size)])

    global_best_particle = copy.copy(empty_particle)
    global_best_particle.fitness = 0

    best_cost_list = []     # we will use this list to plot the best costs at the end
    best_cost_list.append(global_best_particle.fitness)

    # PSO Main Loop
    for itr in range(max_iter):
        for i, particle in enumerate(population):
            # update velocity for binary PSO
            r1 = np.random.random(size = solution_size)
            r2 = np.random.random(size = solution_size)
            particle.velocity = (w * particle.velocity) + (c1 * r1 * (particle.best_position - particle.position)) + (c2 * r2 * (global_best_particle.position - particle.position))

            # apply velocity limits for binary PSO
            particle.velocity = np.clip(particle.velocity, vel_min, vel_max)

            # update position for binary PSO
            particle.position = np.clip(particle.position + particle.velocity, var_min, var_max)

            # update cost and solution
            particle.fitness = objective_func.fitness(w1, particle, cc_parameters, road, main_cars_list, ramp_cars_list)

            # update personal Best
            if particle.fitness < particle.best_fitness:
                particle.best_fitness = particle.fitness
                particle.best_position = particle.position

                # update global Best
                if particle.fitness < global_best_particle.fitness:
                    global_best_particle = copy.copy(particle)

        best_cost_list.append(global_best_particle.fitness)
        print(f"Iteration {itr + 1}: Best Cost: {global_best_particle.fitness}")
        print("Best Solution:", global_best_particle.solution)

        w = w_max - ((w_max - w_min) / max_iter) 
        w = w * 0.8