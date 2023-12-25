import initialization
import cruise_control
import road_class
import vehicle_generation_parameters_class
import Simulation
import random
import sequence 
import performance
import SA
import GA
import DPSO
import Rc_BFFA

#what do you want?
simulate_SA = False
simulate_GA = False
simulate_DPSO = False
simulate_BFFA = True
visualize_simulation = True
get_avarge_time = False
get_all_data = False
num_runs = 10 #for averging 
compare_algos = False

main_cars_num = 10
ramp_cars_num = 5
solution_size = 10

if not get_avarge_time and not get_all_data:
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

#parameters for intalizing cars info --> to make it dynamic
#main_cars_num = random.randint(5,20) #number of main cars generated
#ramp_cars_num = random.randint(5,10) ##numbser of ramp cars generated
#solution_size = random.randint(min(main_cars_num,ramp_cars_num), main_cars_num) #maximum size for the optimization algorithm
#for testing SA with same scenario - delete later

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

algo_list = []
algo_parameters_list = []

#SA Example usage
initial_temperature = 500
final_temperature = 0.05
num_iterations = 100 
iteration_per_temp = 1
#cooling_rate = (final_temperature-initial_temperature) / num_iterations
cooling_rate = 5
linear = True
plot_best = False
SA_exec_time_list = []



SA_parameters = [initial_temperature,
        final_temperature,num_iterations,iteration_per_temp, cooling_rate,linear, main_cars_list, ramp_cars_list,solution_size, weight_func_1,
        highway, cc_parameters,plot_best]



#SA 
if simulate_SA:
    algo_list.append(SA.simulated_annealing)
    algo_parameters_list.append(SA_parameters)
    [SA_temprature_List, SA_fitness_List, best_solution_SA, best_fitness_SA] = SA.simulated_annealing(SA_parameters) 
    #get average excution time 
    if(not compare_algos):
        if not get_all_data:
                print(f"Best SA solution:{best_solution_SA} ")
                print(f"Best SA fitness: {best_fitness_SA}" ) 
        performance.plot_fitness_against_progress(SA_temprature_List, SA_fitness_List, 'Simulated Annealing Algorithm', 'temprature', 'Fitness Value')
    if get_all_data :
        performance.evaluate_performance(SA.simulated_annealing,SA_parameters,num_runs)
        
    elif get_avarge_time:
        SA_avg_execution_time = performance.get_avg_running_time(SA.simulated_annealing,SA_parameters,num_runs)
        print(f"Average SA excution time:  {SA_avg_execution_time} seconds")
        
    #code for visualization
    best_solution_SA_obj = sequence.get_car_object_list_from_sequence(best_solution_SA, main_cars_list, ramp_cars_list)
    #return cars to initial conditions
    for car in list(main_cars_list+ramp_cars_list):
        car.return_to_initial_conditions()
    if visualize_simulation:
        Simulation.visualization(main_cars_list,ramp_cars_list,best_solution_SA_obj,cc_parameters, highway)


# Genetic Algorithm Example usage
population_size = 10
generation_size = 100
crossover_ratio = 0.8
mutation_ratio = 0.1
GA_exec_time_list = []

GA_parameters = [population_size,
        generation_size , crossover_ratio, mutation_ratio, main_cars_list, ramp_cars_list, solution_size, weight_func_1, highway,cc_parameters]

if simulate_GA:
    algo_list.append(GA.genetic_algorithm)
    algo_parameters_list.append(GA_parameters)
    [GA_generation_num, GA_best_fitness_in_generation, best_solution_GA, best_fitness_GA] = GA.genetic_algorithm(GA_parameters)
    if(not compare_algos):     
        if not get_all_data:
                print(f"Best GA solution:{best_solution_GA} ")
                print(f"Best GA fitness: {best_fitness_GA}" ) 
        performance.plot_fitness_against_progress(GA_generation_num, GA_best_fitness_in_generation, 'Genetic Algorithm','generation number', "Best individual's fitness in this generation")
    if get_all_data:
        performance.evaluate_performance( GA.genetic_algorithm, GA_parameters,num_runs)
        
    elif get_avarge_time:
        GA_avg_execution_time = performance.get_avg_running_time(GA.genetic_algorithm,GA_parameters,num_runs)
        print(f"Average GA excution time: ,{GA_avg_execution_time} seconds")
        


    #return cars to initial conditions
    for car in list(main_cars_list + ramp_cars_list):
        car.return_to_initial_conditions()
    best_solution_GA_obj = sequence.get_car_object_list_from_sequence(best_solution_GA, main_cars_list, ramp_cars_list)
    if visualize_simulation:
        Simulation.visualization(main_cars_list,ramp_cars_list,best_solution_GA_obj,cc_parameters, highway)


#discrete PSO
Neighborhood_size = 30
max_iter = 100 #number of iterations
synchronous = False #or Asynchronous
star_topology = False #or ring
c1 = 1.49  # cognitive parameter
c2 = 1.49 # social parameter
#inertia_w = 0.792  # inertia weight intially
vel_max = 6.0 #maximum velocity of a particle

DPSO_parameters = [solution_size, Neighborhood_size, max_iter, c1, c2, synchronous, vel_max,
    star_topology, weight_func_1, cc_parameters, highway, main_cars_list, ramp_cars_list]

if simulate_DPSO:
    algo_list.append(DPSO.discrete_pso)
    algo_parameters_list.append(DPSO_parameters)
    [iterations,best_particle_fitness_list, best_solution_DPSO, best_fitness_DPSO] = DPSO.discrete_pso(DPSO_parameters)
    #print(f"best solution overall {best_solution_overall} and its fitness is {best_fitness_overall}")
    if (not compare_algos):    
            if not get_all_data:
                print(f"Best DPSO solution:{best_solution_DPSO} ")
                print(f"Best DPSO fitness: {best_fitness_DPSO}" ) 
            performance.plot_fitness_against_progress(iterations, best_particle_fitness_list, "Discrete Particle swarm Algorithm",'Time', 'Best Individual Fitness') 

    if get_all_data:
        performance.evaluate_performance( DPSO.discrete_pso, DPSO_parameters,num_runs)
    elif get_avarge_time:
        DPSO_avg_execution_time = performance.get_avg_running_time(DPSO.discrete_pso,DPSO_parameters,num_runs)
        print(f"Average DPSO excution time: ,{DPSO_avg_execution_time} seconds")
        

    #for visualization
    best_solution_DPSO_obj = sequence.get_car_object_list_from_sequence(best_solution_DPSO, main_cars_list, ramp_cars_list)

    #return cars to initial conditions
    for car in list(main_cars_list + ramp_cars_list):
        car.return_to_initial_conditions()

    if visualize_simulation:
        Simulation.visualization(main_cars_list,ramp_cars_list,best_solution_DPSO_obj,cc_parameters, highway)

    #not 2d --> will not work for now
    #plot.plot_DPSO(range(max_iter),best_particle_position_list)    


#Binary Fire Fly Algorthim
population_size = 6
num_of_iteration = 100

BFFA_parameters = [num_of_iteration,population_size,solution_size,main_cars_list,ramp_cars_list,weight_func_1 ,cc_parameters, highway]


if simulate_BFFA:
    algo_list.append(Rc_BFFA.binary_FFA)
    algo_parameters_list.append(BFFA_parameters)
    [iterations, best_fitness_list_BFFA, best_solution_BFFA, best_fitness_BFFA] = Rc_BFFA.binary_FFA(BFFA_parameters)
    if (not compare_algos):
        if not get_all_data:
                print(f"Best BFFA solution:{best_solution_BFFA}")
                print(f"Best BFFA fitness: {best_fitness_BFFA}" ) 
        performance.plot_fitness_against_progress(iterations, best_fitness_list_BFFA, 'Binary Fire FLy Algorithm', 'Generation number', 'Best individual in this generation')
    if get_all_data:
        performance.evaluate_performance(Rc_BFFA.binary_FFA, BFFA_parameters, num_runs)
        
    elif get_avarge_time:
        BFFA_avg_execution_time = performance.get_avg_running_time(Rc_BFFA.binary_FFA,BFFA_parameters,num_runs)
        print(f"Average BFFA excution time: ,{BFFA_avg_execution_time} seconds")
        
    #for visualization
    best_solution_BFFA_obj = sequence.get_car_object_list_from_sequence(best_solution_BFFA, main_cars_list, ramp_cars_list)

    #return cars to initial conditions
    for car in list(main_cars_list + ramp_cars_list):
        car.return_to_initial_conditions()
    if visualize_simulation:
        Simulation.visualization(main_cars_list,ramp_cars_list,best_solution_BFFA_obj,cc_parameters, highway)



#compare different algorithims
if compare_algos:
    performance.compare_fitness(algo_list, algo_parameters_list, 100)
