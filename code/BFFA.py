from objective_func import fitness 
import sequence
import random
import population

def eval_attractiveness(firefly_k, firefly_l, f_max,main_cars_list,ramp_cars_list,w1,cc_parameters,road):
    # Assuming firefly_k and firefly_l are represented as lists of coordinates in the search space
    firefly_l_fitness = fitness(w1, firefly_k, cc_parameters, road, main_cars_list, ramp_cars_list)
    firefly_k_fitness = fitness(w1, firefly_k, cc_parameters, road, main_cars_list, ramp_cars_list)
    
    # Calculate Return
    return_value = (firefly_l_fitness - firefly_k_fitness) / ((f_max - firefly_k_fitness)+0.001)
    #print("evaluation of attractiveness",firefly_k)
    # Calculate Cost
    cost_value = sum(abs(coord_k - coord_l) for coord_k, coord_l in zip(firefly_k,firefly_l))

    #calculate attractiveness based on cost and return 
    attractiveness = 0.5 * ((1 / (cost_value + 1)) + return_value)
    #print(attractiveness)
    #print(firefly_k_fitness)
    return attractiveness


def binary_FFA(t,num_of_iteration,population_size,solution_size,main_cars_list,ramp_cars_list,weight_func_1 ,cc_parameters, road):
    # step 1: generate N initial fireflies in the search space, and evaluate their goodnes
    firefly_population =  population.initialize_population(population_size, solution_size,  main_cars_list ,ramp_cars_list,road, cc_parameters)
    t = 0
    v = []
    #print("firefly_population",firefly_population)
    #Step 2: Update the jump probability
    jump_probabiliry = 0.1 - (0.09*(t/num_of_iteration))
    fitness_list = population.calc_fitness_list(firefly_population, weight_func_1, main_cars_list, ramp_cars_list, cc_parameters, road)
    
    f_max = max(fitness_list)
    non_dominated_fireflies =[]
    #step 3: for each firefly
    for k in range(population_size):  
        attractiveness_list = []  
        for l in range(k,population_size):  
            attractiveness = eval_attractiveness(firefly_population[k], firefly_population[l],f_max,main_cars_list,ramp_cars_list,weight_func_1,cc_parameters,road) 
            attractiveness_list.append(attractiveness)
        sorted_firefly_population_attractiveness = sorted(firefly_population[k:solution_size], key = lambda x:  - attractiveness_list[firefly_population[k:solution_size].index(x)])
    
        non_dominated_fireflies.append(sorted_firefly_population_attractiveness[0])
        attractive_firefly_index = random.randint(0,len(non_dominated_fireflies)-1)
        attractive_firfly = non_dominated_fireflies[attractive_firefly_index]
        attractiveness = eval_attractiveness(firefly_population[k], attractive_firfly, f_max,main_cars_list,ramp_cars_list,weight_func_1,cc_parameters,road)
        
        v = firefly_population[k]
        while(not(sequence.check_feasibility(firefly_population[k], road, cc_parameters, main_cars_list, ramp_cars_list))):   
            for i in range(len(attractive_firfly)):
                rand1 = random.randint(0,1)
                rand2 = random.randint(0,1)
                if attractiveness>rand2:
                    v[i] = attractive_firfly[i]
                if jump_probabiliry>rand1:
                    firefly_population[k][i] = 1 - v[i]
                else:
                    firefly_population[k][i] =  v[i]
        
    
    fitness_list = population.calc_fitness_list(firefly_population, weight_func_1, main_cars_list, ramp_cars_list, cc_parameters, road)
    

    sorted_firefly_population= sorted(firefly_population, key = lambda x:  - fitness_list[firefly_population.index(x)])
    return sorted_firefly_population , sorted(fitness_list,reverse=True)   
                   

