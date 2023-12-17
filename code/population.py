import numpy as np
import math 
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
        #print("random sequence",solution)
         #make sure it is feasibile  
        if sequence.check_feasibility(solution, road,cc_parameters,main_cars_list, ramp_cars_list) : 
            population.append(solution)
            #print("accepted sequence", solution)
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

#returns position not solution
def update_global_best(particles, synchronous, star_topology):
    #get intial global best 
    if synchronous:
        global_best_particle = sorted(particles, key=lambda Particle: Particle.fitness)[0]
        global_best_particle_fitness = global_best_particle.fitness
        global_best_particle_solution = global_best_particle.position
    else :
        global_best_particle_fitness = 0
        global_best_particle_solution = 0

    #assign the instance variables for each particle
    for  particle in particles:
        if not synchronous:
            if particle.fitness > global_best_particle_fitness :
                global_best_particle_fitness = particle.fitness
                global_best_particle_solution = particle.solution
    
        if star_topology:
            particle.Nbest_fitness = global_best_particle_fitness
            particle.solution =  global_best_particle_solution
        #assume ring tobology
        else:
            previous_particle = particles[particles.index(particle) - 1]
            next_particle = particles[particles.index(particle) + 1]
            if previous_particle.fitness > next_particle.fitness :
                particle.Nbest_fitness = previous_particle.fitness
                particle.Nbest_solution = previous_particle.solution
            elif previous_particle.fitness < next_particle.fitness :
                particle.Nbest_fitness = next_particle.fitness
                particle.Nbest_solution = next_particle.solutino

    return global_best_particle_fitness, global_best_particle_solution
        

#using the binary discritaization developed by the creators of pso
def update_motion(particles, c1, c2, vel_max, weight_func_1, cc_parameters, road, main_cars_list, ramp_cars_list):
    for particle in particles:   
        # update fitness (scalar)
        particle.fitness = fitness(weight_func_1, particle.solution, cc_parameters, road, main_cars_list, ramp_cars_list)
        
        # generate random vectors for each particle, (random number for each position of the particle)
        r1 = np.random.random(size = len(particle.solution))
        r2 = np.random.random(size = len(particle.solution))

        # velocity is a vector 
        particle.velocity = (particle.velocity) + (np.dot((c1*r1), (particle.Pbest_position - particle.position))) + np.dot((c2 * r2), (particle.Nbest_position - particle.position))

        #saturate if above max
        particle.velocity = np.clip(particle.velocity, -vel_max, vel_max)

        # update position for binary PSO
        particle.position = particle.position + particle.velocity
        
        # update solution from sigmoid
        new_solution = []
        for x in particle.position:
            sigmoid = 1 / 1 + math.exp(-1 * x)
            r = np.random.rand()
            print(f"velocity : {particle.velocity}, position : {x}, sigmoid : {sigmoid} , and r : {r}")
            if (r < sigmoid):
                new_solution.append(1)
            else:
                new_solution.append(0)
            
        particle.solution = new_solution
        print("new solution", new_solution)
        
        # update personal Best
        if particle.fitness > particle.Pbest_fitness:
            particle.Pbest_fitness = particle.fitness
            particle.Pbest_solution = particle.solution


