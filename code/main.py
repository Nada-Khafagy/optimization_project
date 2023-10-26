from initialization import create_cars
from randomize import randomize_sequence
import merged_platoon
import matplotlib.pyplot as plt
import Simulated_annealing
import platoon
import Simulation

#constraints
min_v_main = 10 * (5/18) #m/s 2.777 
max_v_main = 120 * (5/18) #m/s 33.33
min_v_ramp = 5 * (5/18) #m/s 1.388
max_v_ramp = 120 * (5/18) #m/s33.3
min_a_main = -10 #m/s^2
max_a_main = 10 #m/s^2
min_a_ramp = -8 #m/s^2
max_a_ramp = 8 #m/s^2

#parameters for intalizing cars info
random_pos_lower=5
random_pos_upper=8
merged_sequence_size = 8 #maximum size for the optimization algorithm
cars_main_num = 10 #number of main cars generated
cars_ramp_num = 5 ##number of ramp cars generated
initial_main_v = 60  * 5/18  #m/s
initial_main_a = 3 #m/s^2
initial_ramp_v = 55 * 5/18 #m/s
initial_ramp_a = 0 #m/s^2

#parameters for cruise control
alpha = 1 #k1 for cruise control
beta = 1.2 #k2 for cruise control
gamma = 0.5 #k3for cruise control
desired_distance_bet_cars = 6 #m
decision_position = 40#m, position where we apply cruse control
merging_position = 140 #m, position of point of merging
delta_time = 0.01 #seconds, sampling time

#create cars
(main_cars,ramp_cars) = create_cars(decision_position,initial_main_v,initial_main_a,
                                                      decision_position-10,initial_ramp_v,initial_ramp_a,
                                                      cars_main_num,cars_ramp_num,random_pos_lower,random_pos_upper)
 
#Randomize Solution
def generate_solution(merged_sequence_size, main_cars, ramp_cars, merging_position):
    #assume solution 
    [car_sequence,cars_ramp_merged_no] = randomize_sequence(merged_sequence_size,cars_ramp_num)
    sequence_full_info = dict()
    for i in car_sequence:  
        if i in main_cars:
            sequence_full_info[i] = main_cars[i]
        elif i in ramp_cars :
            sequence_full_info[i] = ramp_cars[i]
    sequence_full_info_list = list(sequence_full_info.values())
    distances_to_merge = []
    for i in range(merged_sequence_size):
        car = sequence_full_info_list[i]        
        distances_to_merge.append(merging_position - car.position)
    #print(distances_to_merge)  
    return  distances_to_merge, cars_ramp_merged_no,sequence_full_info

#check constraints
def check_feasibility(current_solution, min_v_ramp, max_v_ramp, min_a_ramp, max_a_ramp):
    feasibility = True
    while(list(current_solution.values())[merged_sequence_size - 1].position < merging_position): 
        merged_platoon.platooning(current_solution,delta_time,decision_position,merging_position,desired_distance_bet_cars,alpha,beta,gamma)        
        for car in current_solution.values():
            #if it is a main car, use main constraints
            if car.name < chr(97):
                if not car.check_feasibility(min_v_main, max_v_main, min_a_main, max_a_main):
                    return False  
            # if it is a ramp car, use ramp constraints  
            else:
                if not car.check_feasibility(min_v_ramp, max_v_ramp, min_a_ramp, max_a_ramp):
                    return False
    #print(list(current_solution.values())[merged_sequence_size - 1].traveled_time)
    #print(list(current_solution.values())[merged_sequence_size - 1].position )      
    return feasibility



#SA Example usage
initial_temperature = 1000.0
cooling_rate = 0.6
num_iterations = 1000
final_temperature = 0.05
weight_func_1 = 0.5
linear = True
curr_solution = None
curr_objective = 0
best_solution = None
best_objective = 0
best_solution_list=[]
current_solution_list=[]
travel_time=[]
SA_temprature_List = []
SA_obj_func_List = []


iteration_index = -1
#SA Loop
for _ in range(num_iterations):

    #generate new solution
    [distances_to_merge, cars_ramp_merged_no,new_solution_dic] = generate_solution(merged_sequence_size,main_cars,ramp_cars,merging_position)
    #return cars to initial conditions
    for car in new_solution_dic.values():
        car.return_to_initial_conditions()

    #check feasibility
    if (not check_feasibility(new_solution_dic,min_v_ramp, max_v_ramp, min_a_ramp, max_a_ramp)):
          continue
    iteration_index += 1
    #SA for one iteration (if it is better take it if not get temprature and do the other stuff )
    [curr_solution, curr_objective, curr_temperature] = Simulated_annealing.simulated_annealing(iteration_index, curr_solution, curr_objective,
                                        initial_temperature, cooling_rate,linear,
                                        min_v_main,max_v_main,
                                        weight_func_1, cars_ramp_num,cars_ramp_merged_no, new_solution_dic, distances_to_merge)  
     
    if (best_solution is None) or (best_objective < curr_objective) :
        best_solution = curr_solution
        best_objective = curr_objective
   
    if (curr_temperature<=final_temperature):
        break

    SA_temprature_List.append(curr_temperature)
    SA_obj_func_List.append(curr_objective)

    print("Accepted Sequence is: ", [car.name for car in curr_solution.values()] )
    print("current objective:", curr_objective)
    
print("Best solution:", [car.name for car in best_solution.values()])
print("Best objective:", best_objective)


plt.plot(SA_temprature_List,SA_obj_func_List)
# Add labels and a legend
plt.xlabel('temprature')
plt.ylabel('obective function value')
plt.title('Simulated annealing')
plt.gca().invert_xaxis()
# Show the plot (or you can save it to a file with plt.savefig)
plt.show()

    
#changed function parameters, check file before uncommenting
Simulation.visualization(main_cars,ramp_cars,best_solution,delta_time,decision_position,merging_position,desired_distance_bet_cars,alpha,beta,gamma )
#print(objective_func.objective_func(w1,cars_ramp_no,r,sequence_full_info,distances_to_merge,min_v,max_v))

