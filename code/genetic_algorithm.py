import numpy as np
import objective_func
import matplotlib.pyplot as plt
import ga_func
import sequence
import random


def genetic_algorithm(population_size, generation_size , crossover_ratio, mutation_ratio,
        main_cars_list, ramp_cars_list, solution_size, weight_func_1, road,cc_parameters):
    #get number of parents
    #Fitness Based Selection
    elitism_ratio = round(1 - mutation_ratio - crossover_ratio,1)

    population = ga_func.initialize_population(population_size, solution_size, main_cars_list, ramp_cars_list,
                                                                                         road, cc_parameters, weight_func_1)
    fitness_list = ga_func.calc_fitness_list(population, weight_func_1, ramp_cars_list, cc_parameters, road)
    #print("population :",population)
    best_solution = None
    best_fitness = 0
    GA_generation_num = []
    GA_best_sol_in_generation = []
    #print(fitness_list)
    for generation in range(generation_size):
        offspring = []  

        #elits
        #get eliete members and add them
        num_elite = int(elitism_ratio * population_size)
        elite = sorted(population, key = lambda x: - fitness_list[population.index(x)])[:num_elite]
        for sol in elite: 
            offspring.append(sol)

        #Generate offspring through mutations
        #get the worset individuls
        mutations_num = int(mutation_ratio * population_size)
        worst_individuals = sorted(population, key=lambda x: fitness_list[population.index(x)])[:mutations_num]
        #mutate them untill feasable and add them to the new population
        for individual in worst_individuals:
            mutated_feasibility = False
            genes_to_mutate_num = random.randint(0, solution_size)
            while(not mutated_feasibility):
                print("not feasible mutation")
                mutated_inividual = ga_func.mutate(individual,genes_to_mutate_num,main_cars_list, ramp_cars_list, cc_parameters)
                if sequence.check_feasibility(mutated_inividual,road,cc_parameters):
                    offspring.append(mutated_inividual)
                    mutated_feasibility = True


        #cross over
        parents_num = int(crossover_ratio*population_size)
        parents = ga_func.select_parents(parents_num, population, fitness_list)
        # Generate offspring through crossover
        #print("Number of parents is :", len(parents))
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]
            children_feasibility = False
            while(not children_feasibility):
                
                [child1,child2] = ga_func.crossover(parent1, parent2, main_cars_list, ramp_cars_list,cc_parameters) 
                if sequence.check_feasibility(child1,road,cc_parameters) and sequence.check_feasibility(child1,road,cc_parameters) :
                    children_feasibility = True
            offspring.append(child1)
            offspring.append(child2)

        print("length of offspring",len(offspring))

        # Replace the old population with the new one
        #print("new spring is", len(offspring[0]),len(offspring[1]),len(offspring[2]))
        population = offspring
        fitness_list = ga_func.calc_fitness_list(population, weight_func_1, ramp_cars_list, cc_parameters, road)
        print("new fitness list :",fitness_list)
        # Update the best solution found so far
        #print(fitness)
        #print(population[0][1].traveled_time)
        best_solution_index = np.argmax(fitness_list)
        if best_solution is None or fitness_list[best_solution_index] > best_fitness:
            print('best solution index :',best_solution_index)
            print("length of population",len(offspring))
            best_solution = population[best_solution_index]
            best_fitness = fitness_list[best_solution_index]

        GA_generation_num.append(generation)
        GA_best_sol_in_generation.append(best_fitness)

    return GA_generation_num,GA_best_sol_in_generation,best_solution, best_fitness
