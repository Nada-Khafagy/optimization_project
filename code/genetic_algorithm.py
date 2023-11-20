import numpy as np
import objective_func
import matplotlib.pyplot as plt
import ga_func



def genetic_algorithm(main_cars, ramp_cars,population_size, generations,elitism_ratio, crossover_rate, mutation_rate,
                      min_v_main, max_v_main, weight_func_1, cars_ramp_no, solution_size):
    parents_num = int(crossover_rate*population_size)
    [population,cars_ramp_merged_no, distances_to_merge] = ga_func.initialize_population(population_size, solution_size,  main_cars, ramp_cars)

    best_solution = None
    best_objective = 0
    
    for _ in range(generations):
        # Evaluate the fitness of each individual in the population
        offspring = [] 
        print("length of population is:", len(population[0]),len(population[1]),len(population[2]), solution_size)
        fitness = [objective_func.objective_func(weight_func_1, cars_ramp_no, cars_ramp_merged_no, ind,
                                                distances_to_merge, min_v_main, max_v_main) for ind in population]

        # Select parents based on fitness
        num_elite = int(elitism_ratio * population_size)
         # Replace the old population with the new one (excluding elites)
        for i in range(len(population)):
            for car in population[i]:
                car.return_to_initial_conditions()
        elite = sorted(population, key=lambda x: -fitness[population.index(x)])[:num_elite]
        #print("elite is:", elite)
        
        for sol in elite: 
            offspring.append(sol)
        num_mutated = int(mutation_rate * population_size)
        mutated = sorted(population, key=lambda x: fitness[population.index(x)])[:num_mutated]
        ga_func.mutate(mutated)
        for sol in mutated: offspring.append(sol)
        parents = ga_func.select_parents(parents_num,population,weight_func_1, cars_ramp_no,cars_ramp_merged_no,distances_to_merge, min_v_main,max_v_main)

        # Generate offspring through crossover and mutation
        print("Number of parents is :", len(parents))
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]
            [child1,child2] = ga_func.crossover(parent1, parent2)
            offspring.append(child1)
            offspring.append(child2)

        # Replace the old population with the new one
        print("new spring is", len(offspring[0]),len(offspring[1]),len(offspring[2]))
        population = offspring
        print(fitness)
        # Update the best solution found so far
        #print(fitness)
        #print(population[0][1].traveled_time)
        best_solution_index = np.argmax(fitness)
        if best_solution is None or fitness[best_solution_index] > best_objective:
            print(best_solution_index,len(population))
            best_solution = population[best_solution_index]
            best_objective = fitness[best_solution_index]

    return best_solution, best_objective


### The genetic_algorithm function orchestrates the entire Genetic Algorithm. It iterates through generations, evaluates the fitness of each solution, selects parents, performs crossover and mutation to generate offspring, and updates the population. The best solution found during the iterations is returned