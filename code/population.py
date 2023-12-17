import numpy as np
import random
from objective_func import fitness
import sequence
from particle_class import Particle
from copy import copy


#returns solution in binary
def initialize_population(population_size, solution_size,  main_cars_list ,ramp_cars_list,road, cc_parameters):
    population = []
    while (len(population) < population_size):
        # Generate a random solution in binary
        solution = sequence.randomize_sequence(solution_size, len(ramp_cars_list)) 
         #make sure it is feasibile  
        if sequence.check_feasibility(solution, road,cc_parameters,main_cars_list, ramp_cars_list) : 
            population.append(solution)
    return population

#returns a list of fitnesses
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


def update__global_best(particles, synchronous, star_topology):
    #get intial global best 
    if synchronous:
        global_best_particle = sorted(particles, key=lambda Particle: Particle.fitness)[0]
        global_best_particle_fitness = global_best_particle.fitness
        global_best_particle_position = global_best_particle.position
    else :
        global_best_particle_fitness = 0
        global_best_particle_position = 0

    #assign the instance variables for each particle
    for  particle in particles:
        if not synchronous:
            if particle.fitness > global_best_particle_fitness :
                global_best_particle_fitness = particle.fitness
                global_best_particle_position = particle.position
    
        if star_topology:
            particle.Nbest_fitness = global_best_particle_fitness
            particle.Nbest_position =  global_best_particle_position
        #assume ring tobology
        else:
            previous_particle = particles[particles.index(particle) - 1]
            next_particle = particles[particles.index(particle) + 1]
            if previous_particle.fitness > next_particle.fitness :
                particle.Nbest_fitness = previous_particle.fitness
                particle.Nbest_position = previous_particle.position
            elif previous_particle.fitness < next_particle.fitness :
                particle.Nbest_fitness = next_particle.fitness
                particle.Nbest_position = next_particle.position

    return global_best_particle_fitness,global_best_particle_position
        


def update_motion(particles, w, c1, c2, vel_min, vel_max, weight_func_1, cc_parameters, road, main_cars_list, ramp_cars_list):
    for particle in particles:   
        # update velocity for binary PSO
        r1 = np.random.random(size = len(particle.solution))
        r2 = np.random.random(size = len(particle.solution))

        particle.velocity = (w * particle.velocity) + (c1 * r1 * (particle.Pbest_position - particle.position)) + (c2 * r2 * (particle.Nbest_position - particle.position))

        # apply velocity limits for binary PSO
        vel_min = -1.0
        vel_max = 1.0
        particle.velocity = np.clip(particle.velocity, vel_min, vel_max)

        # update position for binary PSO
        particle.position = particle.position + particle.velocity

        # update fitness and solution
        particle.fitness = fitness(weight_func_1, particle, cc_parameters, road, main_cars_list, ramp_cars_list)
        
        # update personal Best
        if particle.fitness > particle.Pbest_fitness:
            particle.Pbest_fitness = particle.fitness
            particle.Pbest_position = particle.position


