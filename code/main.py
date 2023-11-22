from initialization import create_cars
from cruise_control import cruise_control_parameters
import Simulated_annealing
import road_class
import vehicle_generation_parameters_class
import Simulation
import random
import sequence 
from plot import plot_SA
from plot import plot_GA
from genetic_algorithm import genetic_algorithm

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
ramp_cars_num = 10
solution_size = min(main_cars_num,ramp_cars_num)
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
cc_parameters = cruise_control_parameters(decision_position, merging_position, sampling_time, desired_distance_bet_cars,
                                           alpha, beta, gamma)
#collect all parameters in one object, for main and ramp cars
main_car_generation_parameters = vehicle_generation_parameters_class.vehicle_generation_parameters(intial_main_position,
                                            initial_main_velocity, initial_main_accelration, main_cars_num,1, highway)
ramp_car_generation_parameters = vehicle_generation_parameters_class.vehicle_generation_parameters(intial_ramp_position,
                                            initial_ramp_velocity, initial_ramp_accelration, ramp_cars_num,0, highway)

#create cars, save all of their info
main_cars_list = create_cars(main_car_generation_parameters)
ramp_cars_list = create_cars(ramp_car_generation_parameters)

#SA Example usage
initial_temperature = 500
final_temperature = 0.05
num_iterations = 500 
iteration_per_temp = 1
#cooling_rate = (final_temperature-initial_temperature) / maximum_steps_num
cooling_rate = 5
linear = True
plot_best = False

'''
#SA 
[best_solution,best_objective, SA_temprature_List, SA_fitness_List] = Simulated_annealing.simulated_annealing(initial_temperature,
final_temperature,num_iterations,iteration_per_temp, cooling_rate,linear, main_cars_list, ramp_cars_list,solution_size, weight_func_1,
 highway, cc_parameters,plot_best)  
#return cars to initial conditions

print("Best SA solution:", sequence.turn_car_objects_to_binary(best_solution))
print("Best SA objective:", best_objective)

plot_SA(SA_temprature_List,SA_fitness_List)
  
#changed function parameters, check file before uncommenting
Simulation.visualization(main_cars_list,ramp_cars_list,best_solution,cc_parameters)
#print(objective_func.objective_func(w1,cars_ramp_no,r,sequence_full_info,distances_to_merge,min_v,max_v))

'''

# Genetic Algorithm Example usage
population_size = 10
generation_size = 100
crossover_ratio = 0.7
mutation_ratio = 0.2

[GA_generation_num,GA_best_sol_in_generation, best_solution_GA, best_objective_GA] = genetic_algorithm(population_size, generation_size , crossover_ratio, mutation_ratio,
        main_cars_list, ramp_cars_list, solution_size, weight_func_1, highway,cc_parameters)


plot_GA(GA_generation_num, GA_best_sol_in_generation)
for car in list(main_cars_list+ramp_cars_list):
    car.return_to_initial_conditions()
Simulation.visualization(main_cars_list,ramp_cars_list,best_solution_GA,cc_parameters)