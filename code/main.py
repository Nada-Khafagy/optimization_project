from initialization import create_cars
from randomize import randomize_sequence
import merged_platoon
import matplotlib.pyplot as plt
import Simulated_annealing
import platoon
import Simulation
import random

#constraints
min_v_main = 10 * (5/18) #m/s 2.777 
max_v_main = 120 * (5/18) #m/s 33.33
min_v_ramp = 5 * (5/18) #m/s 1.388
max_v_ramp = 120 * (5/18) #m/s33.3
min_a_main = -20 #m/s^2
max_a_main = 20 #m/s^2
min_a_ramp = -20 #m/s^2
max_a_ramp =  20 #m/s^2

#parameters for cruise control
alpha = 1 #k1 for cruise control
beta = 1.2 #k2 for cruise control
gamma = 0.5 #k3for cruise control
desired_distance_bet_cars = 6 #m
decision_position = 40#m, position where we apply cruse control
merging_position = 140 #m, position of point of merging
delta_time = 0.01 #seconds, sampling time

#parameters for intalizing cars info
random_pos_lower = 5
random_pos_upper = 8
cars_main_num = random.randint(5,20) #number of main cars generated
cars_ramp_num = random.randint(5,10) ##number of ramp cars generated
solution_size = random.randint(min(cars_main_num,cars_ramp_num) ,cars_main_num) #maximum size for the optimization algorithm
#for testing SA with same scenario - delete later
cars_main_num = 10
cars_ramp_num = 5 
solution_size = 10
intial_main_p = decision_position - random.randint(10, 30)
intial_ramp_p = decision_position
initial_main_v = 60  * 5/18  #m/s
initial_main_a = 3 #m/s^2
initial_ramp_v = 50 * 5/18 #m/s
initial_ramp_a = 0 #m/s^2



#create cars
(main_cars,ramp_cars) = create_cars(intial_main_p,initial_main_v,initial_main_a,
                                    intial_ramp_p,initial_ramp_v,initial_ramp_a,
                                    cars_main_num,cars_ramp_num,random_pos_lower,random_pos_upper)
#Randomize Solution
def generate_solution(merged_sequence_size, main_cars, ramp_cars, merging_position):
    #assume solution 
    [car_sequence,cars_ramp_merged_no] = randomize_sequence(merged_sequence_size,cars_ramp_num)
    sequence_full_info = dict()
    for car in car_sequence:  
        if car in main_cars:
            sequence_full_info[car] = main_cars[car]
        elif car in ramp_cars :
            sequence_full_info[car] = ramp_cars[car]
        else:
            print("not in both")
    
    distances_to_merge = []
    for car in sequence_full_info.values():    
        distances_to_merge.append(merging_position - car.position)

    return  distances_to_merge, cars_ramp_merged_no,sequence_full_info

#check constraints
def check_feasibility(current_solution, min_v_ramp, max_v_ramp, min_a_ramp, max_a_ramp):
    feasibility = True
    while(list(current_solution.values())[solution_size - 1].position < merging_position): 
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
     
    return feasibility



#SA Example usage
initial_temperature = 500
curr_temperature = initial_temperature
cooling_rate = 3
num_iterations = 1 #for each temp
final_temperature = 0.05
weight_func_1 = 0.7
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
while(curr_temperature > final_temperature):
    #return cars to initial conditions
    for car in main_cars.values():
        car.return_to_initial_conditions()
    for car in ramp_cars.values() :
        car.return_to_initial_conditions()

    #generate new solution
    [distances_to_merge, cars_ramp_merged_no,new_solution_dic] = generate_solution(solution_size,main_cars,ramp_cars,merging_position)
     

    #check feasibility
    if (not check_feasibility(new_solution_dic,min_v_ramp, max_v_ramp, min_a_ramp, max_a_ramp)):
          continue
    iteration_index += 1
    #SA for one iteration (if it is better take it if not get temprature and do the other stuff )
    [curr_solution, curr_objective, curr_temperature] = Simulated_annealing.simulated_annealing(iteration_index, curr_solution, curr_objective,
                                        initial_temperature,curr_temperature, cooling_rate,linear,
                                        min_v_main,max_v_main,
                                        weight_func_1, cars_ramp_num,cars_ramp_merged_no, new_solution_dic, distances_to_merge)  
     
    if (best_solution is None) or (best_objective < curr_objective) :
        best_solution = curr_solution
        best_objective = curr_objective
   
    SA_temprature_List.append(curr_temperature)
    SA_obj_func_List.append(curr_objective)
    
    print("Accepted Sequence is: ", [0 if car.name>=chr(97) else 1 for car in curr_solution.values()] )
    print("current objective:", curr_objective)

print("Best solution:", [0 if car.name>=chr(97) else 1 for car in best_solution.values()])
print("Best objective:", best_objective)


plt.plot(SA_temprature_List,SA_obj_func_List)
# Add labels and a legend
plt.ylim(0, 1)
plt.xlabel('temprature')
plt.ylabel('obective function value')
plt.title('Simulated annealing')
plt.gca().invert_xaxis()
# Show the plot (or you can save it to a file with plt.savefig)
plt.show()

#return cars to initial conditions
for car in main_cars.values():
    car.return_to_initial_conditions()
for car in ramp_cars.values() :
    car.return_to_initial_conditions()
    
#changed function parameters, check file before uncommenting
Simulation.visualization(main_cars,ramp_cars,best_solution,delta_time,decision_position,merging_position,desired_distance_bet_cars,alpha,beta,gamma )
#print(objective_func.objective_func(w1,cars_ramp_no,r,sequence_full_info,distances_to_merge,min_v,max_v))

