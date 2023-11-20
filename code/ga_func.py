import numpy as np
import objective_func
import copy
import random
from objective_func import fitness
from sequence import randomize_sequence
from sequence import get_car_object_list_from_sequence
from sequence import get_distance_to_merge_list
from sequence import check_feasibility
from sequence import turn_binary_to_letters
from sequence import turn_letters_to_binary
from sequence import turn_car_objects_to_letters
from sequence import turn_car_objects_to_binary


def initialize_population(population_size, solution_size, main_cars_list, ramp_cars_list,road, cc_parameters, weight_func_1):
    population = []
    fitness_list = []

    while (len(population) < population_size):
        # Generate a random solution
        [solution, cars_ramp_merged_num] = randomize_sequence(solution_size, len(ramp_cars_list))
        [solution_obj, distances_to_merge_list] = get_car_object_list_from_sequence(solution, main_cars_list, ramp_cars_list, cc_parameters)
        
        if check_feasibility(solution_obj,road,cc_parameters) == True : 
            population.append(solution_obj)
            #print("in the iteration", get_sequence_in_letters_from_cars(solution_obj))
        #append fitness list 
        curr_sol_fitness = fitness(weight_func_1, len(ramp_cars_list),cars_ramp_merged_num,solution_obj,distances_to_merge_list, road)
        fitness_list.append(curr_sol_fitness)
    return population, cars_ramp_merged_num, distances_to_merge_list, fitness_list

# The crossover function takes two parent solutions (parent1 and parent2) 
#and performs crossover to create a child solution. It randomly selects a crossover point and combines
# the information from both parents to create the child solution.

def crossover(parent1, parent2, main_cars_list, ramp_cars_list, cc_parameters):
    # Implement crossover logic to generate offspring from parents
    parent1_binary = turn_car_objects_to_binary(parent1)
    parent2_binary = turn_car_objects_to_binary(parent2)
    crossover_point = np.random.randint(1, len(parent1) - 1)
    child1_binary = (parent1_binary)
    child1_binary[crossover_point:]=((parent2_binary)[crossover_point:])
    child2_binary = (parent2_binary)
    child2_binary[crossover_point:]=((parent1_binary)[crossover_point:])

    child1_letters = turn_binary_to_letters(child1_binary)
    child2_letters = turn_binary_to_letters(child2_binary)
    child1 = get_car_object_list_from_sequence(child1_letters, main_cars_list, ramp_cars_list, cc_parameters)
    child2 = get_car_object_list_from_sequence(child2_letters, main_cars_list, ramp_cars_list, cc_parameters)

    return child1,child2
 
def mutate(bad_cars):
    # Implement mutation logic to perturb the solution
    for sol in bad_cars:
        mutate_point1 = random.randint(0,len(sol)-1)
        mutate_point2 = random.randint(0,len(sol)-1)
        temp = sol[mutate_point2]
        sol[mutate_point2] = sol[mutate_point1]
        sol[mutate_point1]=temp

### 
# The mutate function introduces random changes (mutations) to the solution. It randomly selects two cars and swaps their positions with a probability defined by the mutation_rate.
def select_parents(parents_num,population,weight_func_1, cars_ramp_no,cars_ramp_merged_no,distances_to_merge, min_v_main,max_v_main):
    # Implement your logic for parent selection based on fitness
    fitness_values = [objective_func.objective_func(weight_func_1, cars_ramp_no,cars_ramp_merged_no, solution,distances_to_merge,
                                                     min_v_main,max_v_main) for solution in population]
    total_fitness = sum(fitness_values)
    probabilities = [fitness / total_fitness for fitness in fitness_values]
    parents=[]
    while (len(parents)<parents_num):
        parent = random.choices(population, probabilities)[0]
        if(not(parent in parents)):
            parents.append(parent)
    #while parent2 == parent1:
    #    parent2 = random.choices(population, probabilities)[0]
    #    print("parent1 and parent 2 is",parent1, parent2)
    return parents

###
# The select_parents function is responsible for selecting two parent solutions based on their fitness. It uses a random tournament selection mechanism to choose parents with higher fitness values.


