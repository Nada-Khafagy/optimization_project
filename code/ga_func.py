import numpy as np
import objective_func
import copy
import random
from objective_func import fitness
import sequence


def initialize_population(population_size, solution_size, main_cars_list, ramp_cars_list,road, cc_parameters, weight_func_1):
    population = []

    while (len(population) < population_size):
        # Generate a random solution
        solution = sequence.randomize_sequence(solution_size, len(ramp_cars_list))
        #print(solution)
        solution_obj = sequence.get_car_object_list_from_sequence(solution, main_cars_list,
                                                                                              ramp_cars_list, cc_parameters)  
         #make sure it is feasibile   
        if sequence.check_feasibility(solution_obj,road,cc_parameters) == True : 
            population.append(solution_obj)
            #print("solution accepted")
            #print("in the iteration", get_sequence_in_letters_from_cars(solution_obj))


    return population

def calc_fitness_list(population, weight_func_1, ramp_cars_list, cc_parameters, road):
    fitness_list = []
    for individual in population:
        #print("individial", individual)
        curr_individual_fitness = fitness(weight_func_1, len(ramp_cars_list), individual, cc_parameters, road)
        fitness_list.append(curr_individual_fitness)
    return fitness_list


# The crossover function takes two parent solutions (parent1 and parent2) 
#and performs crossover to create a child solution. It randomly selects a crossover point and combines
# the information from both parents to create the child solution.

def crossover(parent1, parent2, main_cars_list, ramp_cars_list, cc_parameters):
    # Implement crossover logic to generate offspring from parents
    parent1_binary = sequence.turn_car_objects_to_binary(parent1)
    parent2_binary = sequence.turn_car_objects_to_binary(parent2)
    crossover_point = np.random.randint(0, len(parent1) - 1)
    child1_binary = (parent1_binary)
    child1_binary[crossover_point:]=((parent2_binary)[crossover_point:])
    child2_binary = (parent2_binary)
    child2_binary[crossover_point:]=((parent1_binary)[crossover_point:])

    child1_letters = sequence.turn_binary_to_letters(child1_binary)
    child2_letters = sequence.turn_binary_to_letters(child2_binary)
    child1 = sequence.get_car_object_list_from_sequence(child1_letters, main_cars_list, ramp_cars_list, cc_parameters)
    child2 = sequence.get_car_object_list_from_sequence(child2_letters, main_cars_list, ramp_cars_list, cc_parameters)

    return child1,child2
 
# The mutate function introduces random changes (mutations) to the solution. 
# It randomly selects two cars and swaps their positions with a probability defined by the mutation_rate.
#mutates only one individual
def mutate(bad_sol,genes_to_mutate_num,main_cars_list, ramp_cars_list, cc_parameters):
    bad_sol_binary = sequence.turn_car_objects_to_binary(bad_sol)
    random_indices = random.sample(range(len(bad_sol)), genes_to_mutate_num)
    # Flip the values at the randomly selected indices
    for index in random_indices:
        probability_to_change = random.random()
        if probability_to_change > 0.5:
            bad_sol_binary[index] = 1 - bad_sol_binary[index]  #flip 0 to 1 , and 1 to 0

    bad_sol_letters = sequence.turn_binary_to_letters(bad_sol_binary)
    bad_sol = sequence.get_car_object_list_from_sequence(bad_sol_letters, main_cars_list, ramp_cars_list, cc_parameters)
    return bad_sol


# The select_parents function is responsible for selecting two parent solutions based on their fitness.
# It uses a random tournament selection mechanism to choose parents with higher fitness values.
def select_parents(parents_num, population,fitness_list ):
    #Roulette Wheel Selection
    fitness_list_copy = list(fitness_list)
    total_fitness = sum(fitness_list_copy)
    probabilities = [fitness / total_fitness for fitness in fitness_list]
    parents = []
    #while (len(parents) < parents_num):
    #    parent = random.choices(population, probabilities)[0]
    #    if(not(parent in parents)):
    #        parents.append(parent)
    #while parent2 == parent1:
    #    parent2 = random.choices(population, probabilities)[0]
    #    print("parent1 and parent 2 is",parent1, parent2)
    for _ in range(parents_num):

        probabilities = [fitness / total_fitness for fitness in fitness_list_copy]     
        # Use random.choices to select an individual based on probabilities
        parent = random.choices(population, probabilities)[0]      
        # Append the selected parent to the list
        parents.append(parent)      
        # Remove the selected parent from the population
        index_to_remove = population.index(parent)
        population.remove(parent)
        fitness_list_copy.remove(fitness_list_copy[index_to_remove])
        # Recalculate total_fitness for the updated population
        total_fitness = sum(fitness_list_copy)
    
    return parents




