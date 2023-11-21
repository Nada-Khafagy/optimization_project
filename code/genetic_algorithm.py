import numpy as np
import objective_func
import matplotlib.pyplot as plt
import ga_func



def genetic_algorithm(population_size, generations,elitism_ratio, crossover_rate,mutation_rate,
        main_cars_list, ramp_cars_list,solution_size, weight_func_1, road,cc_parameters):
    #get number of parents
    parents_num = int(crossover_rate*population_size)
    [population, cars_ramp_merged_num, distances_to_merge_list, fitness_list] = ga_func.initialize_population(population_size, solution_size, main_cars_list, ramp_cars_list,
                                                                                         road, cc_parameters, weight_func_1)

    best_solution = None
    best_objective = 0
    
    for _ in range(generations):
        
        offspring = []         
        # Select parents based on fitness
        num_elite = int(elitism_ratio * population_size)
        #get eliete members and add them
        elite = sorted(population, key=lambda x: - fitness_list[population.index(x)])[:num_elite]
        #print("elite is:", elite)
        for sol in elite: 
            offspring.append(sol)
        #get the worse individuls
        mutations_num = int(mutation_rate * population_size)
        mutated = sorted(population, key=lambda x: fitness_list[population.index(x)])[:mutations_num]
        #mutate them and then to the new population
        mutated = ga_func.mutate(mutated,mutations_num,main_cars_list, ramp_cars_list, cc_parameters)
        for sol in mutated:
            offspring.append(sol)

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
