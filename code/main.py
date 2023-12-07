import time
import initialization
import cruise_control
import Simulated_annealing
import road_class
import vehicle_generation_parameters_class
import Simulation
import random
import sequence 
import plot
import genetic_algorithm
import discrete_pso

#what do you want?
simulate_SA = False
simulate_GA = False
simulate_PSO = True
visualize_simulation = False
get_avarge_time = False
num_runs = 100

if not get_avarge_time:
    num_runs = 1

#constraints
min_v_main = 10 * (5/18) #m/s 2.777 
max_v_main = 120 * (5/18) #m/s 33.33
min_v_ramp = 5 * (5/18) #m/s 1.388
max_v_ramp = 120 * (5/18) #m/s33.3 
min_a_main = -20 #m/s^2
max_a_main = 20 #m/s^2
min_a_ramp = -20 #m/s^2
max_a_ramp =  20 #m/s^2
position_lower_limit = 5
position_upper_limit = 8
#objective function
weight_func_1 = 0.7

#parameters for cruise control
decision_position = 40 #m, position where we start applying cruise control
merging_position = 140 #m, position of point of merging
sampling_time = 0.01 #seconds
desired_distance_bet_cars = 6 #m
alpha = 1 #k1 for cruise control
beta = 1.2 #k2 for cruise control
gamma = 0.5 #k3 for cruise control

#parameters for intalizing cars info
main_cars_num = random.randint(5,20) #number of main cars generated
ramp_cars_num = random.randint(5,10) ##number of ramp cars generated
solution_size = random.randint(min(main_cars_num,ramp_cars_num), main_cars_num) #maximum size for the optimization algorithm
#for testing SA with same scenario - delete later
main_cars_num = 10
ramp_cars_num = 5
solution_size = 10
#main cars intial parameters
intial_main_position = decision_position - random.randint(10, 30)
initial_main_velocity = 60  * 5/18  #m/s
initial_main_accelration = 3 #m/s^2
#ramp cars inital parameters
intial_ramp_position = decision_position
initial_ramp_velocity = 50 * 5/18 #m/s
initial_ramp_accelration = 0 #m/s^2


#create a road object with the maximum values for cars
highway = road_class.Road(min_v_main,max_v_main,min_v_ramp,max_v_ramp,min_a_main,max_a_main,min_a_ramp, max_a_ramp,
                           position_lower_limit, position_upper_limit)
#create cruise contol parameters 
cc_parameters = cruise_control.cruise_control_parameters(decision_position, merging_position, sampling_time, desired_distance_bet_cars,
                                           alpha, beta, gamma)
#collect all parameters in one object, for main and ramp cars
main_car_generation_parameters = vehicle_generation_parameters_class.vehicle_generation_parameters(intial_main_position,
                                            initial_main_velocity, initial_main_accelration, main_cars_num,1, highway)
ramp_car_generation_parameters = vehicle_generation_parameters_class.vehicle_generation_parameters(intial_ramp_position,
                                            initial_ramp_velocity, initial_ramp_accelration, ramp_cars_num,0, highway)

#create cars, save all of their info
main_cars_list = initialization.create_cars(main_car_generation_parameters)
ramp_cars_list = initialization.create_cars(ramp_car_generation_parameters)

#SA Example usage
initial_temperature = 1000
final_temperature = 0.05
num_iterations = 1000 
iteration_per_temp = 1
#cooling_rate = (final_temperature-initial_temperature) / num_iterations
cooling_rate = 5
linear = True
plot_best = False
SA_exec_time_list = []


#SA 
if simulate_SA:
    for _ in range(num_runs):
        SA_start_time = time.time()
        [best_solution_SA,best_objective_SA, SA_temprature_List, SA_fitness_List] = Simulated_annealing.simulated_annealing(initial_temperature,
        final_temperature,num_iterations,iteration_per_temp, cooling_rate,linear, main_cars_list, ramp_cars_list,solution_size, weight_func_1,
        highway, cc_parameters,plot_best) 
        SA_end_time = time.time() 
        SA_execution_time = SA_end_time - SA_start_time
        SA_exec_time_list.append(SA_execution_time)
        print(f"SA excution time for run {_} :", SA_execution_time)
        print("Best SA solution:", best_solution_SA)
        print("Best SA fitness:", best_objective_SA)
    
    #get average excution time 
    SA_avg_execution_time = sum(SA_exec_time_list)/len(SA_exec_time_list)
    print("Average SA excution time: ", SA_avg_execution_time)

    plot.plot_SA(SA_temprature_List, SA_fitness_List)

        #return cars to initial conditions
    for car in list(main_cars_list+ramp_cars_list):
        car.return_to_initial_conditions()
    best_solution_SA_obj = sequence.get_car_object_list_from_sequence(best_solution_SA, main_cars_list, ramp_cars_list)
    if visualize_simulation:
        Simulation.visualization(main_cars_list,ramp_cars_list,best_solution_SA_obj,cc_parameters)




# Genetic Algorithm Example usage
population_size = 10
generation_size = 100
crossover_ratio = 0.8
mutation_ratio = 0.1
GA_exec_time_list = []

if simulate_GA:
    for _ in range(num_runs):
        GA_start_time = time.time()
        [GA_best_sol_in_generation, best_solution_GA, best_objective_GA] = genetic_algorithm.genetic_algorithm(population_size,
        generation_size , crossover_ratio, mutation_ratio, main_cars_list, ramp_cars_list, solution_size, weight_func_1, highway,cc_parameters)
        GA_end_time = time.time() 
        GA_execution_time = GA_end_time - GA_start_time
        GA_exec_time_list.append(GA_execution_time)
        print(f"GA excution time for run {_} :",GA_execution_time)
        print("Best GA solution:", best_solution_GA)
        print("Best GA fitness:", best_objective_GA)

    GA_avg_execution_time = sum(GA_exec_time_list)/len(GA_exec_time_list)
    print("Average GA excution time: ", GA_avg_execution_time)

    plot.plot_GA(range(generation_size), GA_best_sol_in_generation)
    #return cars to initial conditions
    for car in list(main_cars_list + ramp_cars_list):
        car.return_to_initial_conditions()

    best_solution_GA_obj = sequence.get_car_object_list_from_sequence(best_solution_GA, main_cars_list, ramp_cars_list)
    if visualize_simulation:
        Simulation.visualization(main_cars_list,ramp_cars_list,best_solution_GA_obj,cc_parameters)


#discrete PSO
var_min = 0 # Lower Bound of Variables
var_max = 1 # Upper Bound of Variables
Neighborhood_size = 30
max_iter = 100
synchronous = False 
varying_w = True
star_topology = True
c1 = 1.49  # cognitive parameter
c2 = 1.49 # social parameter
inertia_w = 0.792  # inertia weight intially
w_min = 0.2  # Minimum inertia weight
max_iter = 100  # Maximum number of iterations
vel_min = -1.0 #minimum velocity of a particle
vel_max = 1.0 #maximum velocity of a particle





if simulate_PSO:
    [] = discrete_pso.discrete_pso(solution_size, var_min, var_max, Neighborhood_size, max_iter, inertia_w, c1, c2, synchronous,
                                   w_min, vel_min, vel_max, star_topology,varying_w ,weight_func_1, cc_parameters, highway,
                                     main_cars_list, ramp_cars_list)
