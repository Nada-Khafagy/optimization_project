import numpy as np
import math
import copy
import matplotlib.pyplot as plt
from problem import problem
import sequence
import time
import initialization
import cruise_control
import road_class
import vehicle_generation_parameters_class
import Simulation
import random
import sequence
import plot
import ant_colony_optimization
def fitness(w1, ramp_cars_total_num, obj_sequence, cc_paramters,road):
    #just to make sure everything is correct
    for car in obj_sequence:
        car.return_to_initial_conditions()

    distances_to_merge = sequence.get_distance_to_merge_list(obj_sequence, cc_paramters)
    
    if not sequence.check_feasibility( obj_sequence, road, cc_paramters):
        return -1

    ramp_cars_used=0
    for car in obj_sequence:
        if car.name >= chr(97):
            ramp_cars_used+=1

    f1 = ramp_cars_used / ramp_cars_total_num
    sum1 = 0
    sum2 = 0
    sum3 = 0

    for car, distance in zip(obj_sequence,distances_to_merge):
        if car.name >= chr(97):
            continue
        sum1 = sum1 + car.traveled_time
        #if distances_to_merge[i] < 0:
            #print('Sum2 is negative !!!!!!!')

        sum2 = sum2 + (distance/road.min_v_main)
        sum3 = sum3 + (distance/road.max_v_main)

    if sum2 == sum3: #no main line cars on solution, maybe we change this later
        f2 = 0
    else:
        f2 = (sum2-sum1) / (sum2-sum3)

    w2 = 1 - w1
    value = (w1 * f1) + (w2 * f2)

    '''print("value of sum1 :", sum1)
    print("value of sum2 :", sum2)
    print("value of sum3 :", sum3)
    print("value of F1 :", f1)
    print("value of F2 :", f2)
    print("cost ", value)'''

    return value
#parameters for cruise control
decision_position = 40 #m, position where we start applying cruise control
merging_position = 140 #m, position of point of merging
sampling_time = 0.01 #seconds
desired_distance_bet_cars = 6 #m
alpha = 1 #k1 for cruise control
beta = 1.2 #k2 for cruise control
gamma = 0.5 #k3 for cruise control

cc_parameters = cruise_control.cruise_control_parameters(decision_position, merging_position, sampling_time, desired_distance_bet_cars,
                                           alpha, beta, gamma)

P = 1000
M = 8
nVar = 5              # Number of Decision Variables
varSize = nVar        # Size of Decision Variable Matrix
varMin = 0            # Lower Bound of Variables
varMax = 1            # Upper Bound of Variables
nPop = 50

# Other PSO parameters
max_iter = 100
c1 = 2.0  # cognitive parameter
c2 = 2.0  # social parameter
w = 0.5   # inertia weight
vel_min = -1.0
vel_max = 1.0
w_max = 0.9  # Maximum inertia weight
w_min = 0.2  # Minimum inertia weight
max_iter = 100  # Maximum number of iterations

class Particle:
    pass

def initialize_particle(varSize):
    particle = Particle()
    particle.position = np.random.randint(2, size=varSize)  # Initialize binary positions (0 or 1)
    particle.velocity = np.zeros(shape=varSize)
    particle.solution = []  # Initialize the solution attribute
    particle.cost, particle.solution = fitness(*particle.position, P, M, cc_parameters)
    particle.best_position = particle.position
    particle.best_cost = particle.cost
    return particle

empty_particle = initialize_particle(varSize)

# Create a population of empty particles:
pop = np.array([initialize_particle(varSize) for _ in range(nPop)])

global_best_particle = copy.copy(empty_particle)
global_best_particle.cost = math.inf

best_cost_list = []     # we will use this list to plot the best costs at the end
best_cost_list.append(global_best_particle.cost)

# PSO Main Loop
for itr in range(max_iter):
    for i, particle in enumerate(pop):
        # update velocity for binary PSO
        r1 = np.random.random(size=varSize)
        r2 = np.random.random(size=varSize)
        particle.velocity = (w * particle.velocity) + (c1 * r1 * (particle.best_position - particle.position)) + (c2 * r2 * (global_best_particle.position - particle.position))

        # apply velocity limits for binary PSO
        particle.velocity = np.clip(particle.velocity, vel_min, vel_max)

        # update position for binary PSO
        particle.position = np.clip(particle.position + particle.velocity, varMin, varMax)

        # update cost and solution
        particle.cost, particle.solution = fitness(*particle.position, P, M)

        # update personal Best
        if particle.cost < particle.best_cost:
            particle.best_cost = particle.cost
            particle.best_position = particle.position

            # update global Best
            if particle.cost < global_best_particle.cost:
                global_best_particle = copy.copy(particle)

    best_cost_list.append(global_best_particle.cost)
    print(f"Iteration {itr + 1}: Best Cost: {global_best_particle.cost}")
    print("Best Solution:", global_best_particle.solution)

    w = w_max - ((w_max - w_min) / max_iter) 
    w = w * 0.8

plt.plot(best_cost_list)
plt.title('Cost')
plt.xlabel('Iterations')
plt.ylabel('Cost (Linear)')

plt.figure()
plt.semilogy(best_cost_list)
plt.title('Cost')
plt.xlabel('Iterations')
plt.ylabel('Cost (Semilog)')
plt.show()

print('Finished')