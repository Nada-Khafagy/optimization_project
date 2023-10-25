import initialization
import objective_func
import platoon
import randomize_sequence
import Simulation
import SA
import merged_platoon
import matplotlib.pyplot as plt
import Simulated_annealing
#import Whole_Systme


#global variables
alpha = 10
beta = 20
gamma = 20
decision_position = 40#m, position where we apply cruse control
merging_position = 140 #m, position of point of merging
delta_time = 0.01 #seconds, sampling time

#constraints
min_v = 10 * (5/18) #m/s
max_v = 120 * (5/18) #m/s
min_v_ramp = 5 * (5/18) #m/s
max_v_ramp = 120 * (5/18) #m/s
min_a_ramp = -3 #m/s^2
max_a_ramp = 3 #m/s^2
min_a = -6 #m/s^2
max_a = 5 #m/s^2


#initalize intlizing parameters for cars info
merged_sequence_size = 8 #maximum size for the optimization algorithm
cars_main_line_no = 10 #number of main line generated cars
cars_ramp_no = 5
initial_main_v = 60  * 5/18  #m/s
initial_main_a = 3 #m/s^2

initial_ramp_v = 55 * 5/18 #m/s
initial_ramp_a = 0 #m/s^2


(main_cars,ramp_cars) = initialization.initalize_cars(decision_position,initial_main_v,initial_main_a,
                                                      decision_position-10,initial_ramp_v,initial_ramp_a,
                                                      cars_main_line_no,cars_ramp_no)



def generate_solution(merged_sequence_size, main_cars, ramp_cars, merging_position):
    #assume solution 
    [car_sequence,cars_ramp_merged_no] = randomize_sequence.randomize(merged_sequence_size)
    sequence_full_info = dict()
    for i in car_sequence:  
        if i in main_cars:
            sequence_full_info[i] = main_cars[i]
        elif i in ramp_cars :
            sequence_full_info[i] = ramp_cars[i]
    sequence_full_info_list = list(sequence_full_info.values())
    #Simulation.platooning(main_cars,ramp_cars,sequence_full_info)
    distances_to_merge = []
    for i in range(merged_sequence_size):
        car = sequence_full_info_list[i]
        distances_to_merge.append(merging_position - car.position)
    #print(distances_to_merge)
    return sequence_full_info_list, distances_to_merge, cars_ramp_merged_no,sequence_full_info


def check_feasibility(current_solution, min_v_ramp, max_v_ramp, min_a_ramp, max_a_ramp):
    feasibility = True
    while(list(current_solution.values())[merged_sequence_size - 1].position < merging_position):    
        merged_platoon.platooning(current_solution, delta_time)
        for car in current_solution.values():
            print(car.traveled_time)
            print(car.velocity)
            print(car.acceleration)
            #if it is a main car, use main constraints
            if car.name >= chr(97):
                if not car.check_feasibility(min_v, max_v, min_a, max_a):
                    return False  
            # if it is a ramp car, use ramp constraints  
            else:
                if not car.check_feasibility(min_v_ramp, max_v_ramp, min_a_ramp, max_a_ramp):
                    return False

    return feasibility

#cruise control 
'''while(sequence_full_info_list[merged_sequence_size-1].position < merging_position):    
    merged_platoon.platooning(sequence_full_info,delta_time)

for car in sequence_full_info_list:
    if not car.check_feasibility:
        print("not feasable")
        break

'''    


#Simulation.platooning(main_cars,ramp_cars,sequence_full_info)
#print(objective_func.objective_func(w1,cars_ramp_no,r,sequence_full_info,distances_to_merge,min_v,max_v))



'''[best_solution, best_objective, SA_temprature_List, SA_obj_func_List]= SA.simulated_annealing(delta_time, decision_position,initial_main_v,initial_main_a,initial_ramp_v,initial_ramp_a,cars_main_line_no, merging_position,
                        cars_ramp_no, merged_sequence_size ,  initial_temperature, final_temperature, cooling_rate, num_iterations,
                          min_v,max_v,min_a,max_a,min_v_ramp,max_v_ramp,min_a_ramp,max_a_ramp, linear,w1, cars_ramp_no,distances_to_merge)

plt.plot(SA_temprature_List, SA_obj_func_List,label='Data Points', color='red', marker='o')
# Add labels and a legend
plt.xlabel('x')
plt.ylabel('y')
plt.title('Plot of a Function')
plt.legend()

# Show the plot (or you can save it to a file with plt.savefig)
plt.show()'''

#SA Example usage
initial_temperature = 100.0
cooling_rate = 0.6
num_iterations = 1 
final_temperature = 5

w1 = 0.5
rl = 1
min_v = 60  * 5/18 #m/s
max_v = 120 * (5/18) #m/s
linear = True


current_solution = None
current_objective = None
best_solution = None
best_objective = None
flag_finish=True
first_iteration=False
k=0
solution_list=[]
travel_time=[]
for j in range(num_iterations):
    #generate new solution
    [new_solution, distances_to_merge, cars_ramp_merged_no,new_solution_dic] = generate_solution(merged_sequence_size,main_cars,ramp_cars,merging_position) 
    #check feasibility
    if (not check_feasibility(new_solution_dic,min_v_ramp, max_v_ramp, min_a_ramp, max_a_ramp)):
          k=1
        
    #SA for one iteration (if it is better take it if not get temprature and do the other stuff )
    if j==0:
        first_iteration = True
    [current_solution, current_objective,flag_finish] = Simulated_annealing.simulated_annealing(delta_time,merging_position,merged_sequence_size,num_iterations,first_iteration,
                                        initial_temperature, final_temperature, cooling_rate,linear,
                                        min_v,max_v,min_a,max_a,min_v_ramp,max_v_ramp,min_a_ramp,max_a_ramp,
                                        w1, cars_ramp_no,cars_ramp_merged_no, new_solution_dic,new_solution, distances_to_merge)   
    if (best_solution is None) or (best_objective < current_objective) :
        best_solution = current_solution
        best_objective = current_objective
   
    if (flag_finish==True):
        break
for i in best_solution.values():
    solution_list.append(i.name)
    travel_time.append(i.traveled_time)
print("Best solution:", solution_list)
print("Best objective:", best_objective)
print("Best Travel Time:", travel_time)
    

    