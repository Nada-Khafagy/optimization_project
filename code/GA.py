import numpy as np
import objective_func
import matplotlib.pyplot as plt
import population
import sequence
import random


def genetic_algorithm(GA_parameters):
    population_size, generation_size , crossover_ratio, mutation_ratio, main_cars_list, ramp_cars_list, solution_size, weight_func_1, road,cc_parameters = GA_parameters[:]
    #get number of parents
    #Fitness Based Selection
    elitism_ratio = round(1 - mutation_ratio - crossover_ratio,1)
    GA_population = population.initialize_population(population_size, solution_size, main_cars_list, ramp_cars_list,road, cc_parameters)
    fitness_list = population.calc_fitness_list(GA_population, weight_func_1, main_cars_list, ramp_cars_list, cc_parameters, road)

    best_solution_overall = None
    best_fitness_overall = 0

    
    GA_best_fitness_in_generation = []
    prev_elite = []

    for _ in range(generation_size):
        offspring = []  
        #get eliete members and add them
        num_elite = int(elitism_ratio * population_size)
        #print("num of elits", num_elite)
        elite = sorted(GA_population, key = lambda x: - fitness_list[GA_population.index(x)])[:num_elite]
        for sol in elite: 
            offspring.append(sol)

        #Generate offspring through mutations
        mutations_num = int(mutation_ratio * population_size)
        #print("mutations_num", mutations_num)
        #get the worset individuls
        worst_individuals = sorted(GA_population, key=lambda x: fitness_list[GA_population.index(x)])[:mutations_num]
        #mutate them untill feasable and add them to the new population
        for individual in worst_individuals:
            mutated_feasibility = False
            genes_to_mutate_num = random.randint(0, solution_size)
            while(not mutated_feasibility):
                mutated_inividual = population.mutate(individual,genes_to_mutate_num)
                if sequence.check_feasibility(mutated_inividual, road, cc_parameters, main_cars_list, ramp_cars_list ):
                    offspring.append(mutated_inividual)
                    mutated_feasibility = True
                    break
                #print("not feasible mutation")
        #print("len(offspring)", len(offspring))

        #cross over
        children_num = int(crossover_ratio*population_size)
        #print("cross over num", children_num)
        #convert to highest even number to get number of parent
        parents_num = children_num
        parents_num += 1 if children_num % 2 != 0 else 0
        #select parent to cross over
        parents = population.select_parents(parents_num, GA_population, fitness_list)
        # Generate offspring through crossover
        #print("Number of parents is :", len(parents))
        for index in range(0, len(parents), 2):
            parent1 = parents[index]
            parent2 = parents[index + 1]
            children_feasibility = False
            while(not children_feasibility):                
                [child1,child2] = population.crossover(parent1, parent2) 
                child1_is_feasibile = sequence.check_feasibility(child1,road,cc_parameters, main_cars_list, ramp_cars_list)
                child2_is_feasibile = sequence.check_feasibility(child2,road,cc_parameters, main_cars_list, ramp_cars_list)     
                children_feasibility = child1_is_feasibile and child2_is_feasibile 
                #print("not feasible childeren")
            offspring.append(child1)
            #in case of odd num of children, don't add the second child
            if ((index == (len(parents)-2)) and (children_num % 2 == 1)) :
                break
            else:
                offspring.append(child2)
        #print("len(offspring)", len(offspring))
        #print("prev elite",  prev_elite)

        # Replace the old population with the new one
        #print(elite[0] in offspring)
        #prev_elite = elite
        GA_population = offspring
        #print("population size :", len(GA_population))
        fitness_list = population.calc_fitness_list(GA_population, weight_func_1, main_cars_list, ramp_cars_list, cc_parameters, road)


        best_solution_index_per_iteration = np.argmax(fitness_list)
        # Update the best solution found so far
        if (best_solution_overall is None or fitness_list[best_solution_index_per_iteration] > best_fitness_overall):
            best_solution_overall = GA_population[best_solution_index_per_iteration]
            best_fitness_overall = fitness_list[best_solution_index_per_iteration]

         
        #update generation best
        #print(fitness_list[best_solution_index_per_iteration])

        GA_best_fitness_in_generation.append(fitness_list[best_solution_index_per_iteration])
        #print('best solution in this iteration is :',fitness_list[best_solution_index_per_iteration])
        #print("prev elite",  prev_elite)

    return range(generation_size), GA_best_fitness_in_generation, best_solution_overall, best_fitness_overall
