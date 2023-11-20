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
from sequence import get_sequence_in_letters_from_cars


def initialize_population(population_size, solution_size, ramp_cars_num, main_cars_list, ramp_cars_list,road, cc_parameters , weight_func_1):
    population = []
    fitness_list = []

    while (len(population) < population_size):
        # Generate a random solution
        [solution, cars_ramp_merged_num] = randomize_sequence(solution_size, ramp_cars_num)
        [solution_obj, distances_to_merge_list] = get_car_object_list_from_sequence(solution, main_cars_list, ramp_cars_list, cc_parameters)
        
        if check_feasibility(solution_obj,road,cc_parameters) == True : 
            population.append(solution_obj)
            #print("in the iteration", get_sequence_in_letters_from_cars(solution_obj))
        #append fitness list 
        curr_sol_fitness = fitness(weight_func_1, len(ramp_cars_list),cars_ramp_merged_num,solution_obj,distances_to_merge_list, road)
        fitness_list.append(curr_sol_fitness)

        #return car objects to their initial condition before getting a new solution
        for car in solution_obj:
            car.return_to_initial_conditions()

    return population, cars_ramp_merged_num, distances_to_merge_list, fitness_list


def crossover(parent1, parent2):
    # Implement crossover logic to generate offspring from parents
    crossover_point = np.random.randint(1, len(parent1) - 1)
    child1 = (parent1)
    child1[crossover_point:]=((parent2)[crossover_point:])
    child2 = (parent2)
    child2[crossover_point:]=((parent1)[crossover_point:])

    return child1,child2
 
# The crossover function takes two parent solutions (parent1 and parent2) 
#and performs crossover to create a child solution. It randomly selects a crossover point and combines
# the information from both parents to create the child solution.

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
    while len(parents) <  (parents_num):
        parent = random.choices(population, probabilities)[0]
        if(not(parent in parents)):
            parents.append(parent)
    #while parent2 == parent1:
    #    parent2 = random.choices(population, probabilities)[0]
    #    print("parent1 and parent 2 is",parent1, parent2)
    return parents

###
# The select_parents function is responsible for selecting two parent solutions based on their fitness. It uses a random tournament selection mechanism to choose parents with higher fitness values.

