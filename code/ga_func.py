import numpy as np
import objective_func
import copy
import random
from objective_func import fitness
import sequence

#returns solution in binary
def initialize_population(population_size, solution_size,  main_cars_list ,ramp_cars_list,road, cc_parameters, weight_func_1):
    population = []
    while (len(population) < population_size):
        # Generate a random solution in binary
        solution = sequence.randomize_sequence(solution_size, len(ramp_cars_list)) 
         #make sure it is feasibile  
        if sequence.check_feasibility(solution, road,cc_parameters,main_cars_list, ramp_cars_list) : 
            population.append(solution)
    return population

def calc_fitness_list(population, weight_func_1, main_cars_list, ramp_cars_list, cc_parameters, road):
    fitness_list = []
    for individual in population:
        #print("individial", individual)
        curr_individual_fitness = fitness(weight_func_1, individual, cc_parameters, road, main_cars_list, ramp_cars_list)
        if curr_individual_fitness != -1:
            fitness_list.append(curr_individual_fitness)
        else:
            print("a solution is not feasable")
    return fitness_list


# The crossover function takes two parent solutions (parent1 and parent2) 
#and performs crossover to create a child solution. It randomly selects a crossover point and combines
# the information from both parents to create the child solution.

def crossover(parent1, parent2):
    # Implement crossover logic to generate offspring from parents
    crossover_point = np.random.randint(0, len(parent1) - 1)
    child1 = list(parent1)
    child1[crossover_point:]=((parent2)[crossover_point:])
    child2 = list(parent2)
    child2[crossover_point:]=((parent1)[crossover_point:])

    return child1,child2
 
# The mutate function introduces random changes (mutations) to the solution. 
# It randomly selects two cars and swaps their positions with a probability defined by the mutation_rate.
#mutates only one individual returns binary
def mutate(bad_sol, genes_to_mutate_num):
    mutated = list(bad_sol)
    random_indices = random.sample(range(len(mutated)), genes_to_mutate_num)
    # Flip the values at the randomly selected indices
    for index in random_indices:
        probability_to_change = random.random()
        if probability_to_change > 0.5:
            mutated[index] = 1 - mutated[index]  #flip 0 to 1 , and 1 to 0
    return mutated


# The select_parents function is responsible for selecting two parent solutions based on their fitness.
# It uses a random tournament selection mechanism to choose parents with higher fitness values.
def select_parents(parents_num, population, fitness_list):
    #Roulette Wheel Selection
    fitness_list_copy = list(fitness_list)
    population_list_copy = list(population)
    total_fitness = sum(fitness_list_copy)
    probabilities = [fitness / total_fitness for fitness in fitness_list]
    parents = []
    #we don't consider the probability for those who were already selected in our implementation
    for _ in range(parents_num):
        probabilities = [fitness / total_fitness for fitness in fitness_list_copy]     
        # Use random.choices to select an individual based on probabilities
        parent = random.choices(population_list_copy, probabilities)[0]      
        # Append the selected parent to the list
        parents.append(parent)
        # Remove the selected parent from the population
        index_to_remove = population_list_copy.index(parent)
        population_list_copy.remove(parent)
        fitness_list_copy.remove(fitness_list_copy[index_to_remove])
        # Recalculate total_fitness for the updated population
        total_fitness = sum(fitness_list_copy)  
    return parents




