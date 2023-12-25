from objective_func import fitness 
import sequence
import random
import population


def binary_FFA(BFFA_parameters):
    num_of_iteration,population_size,solution_size,main_cars_list,ramp_cars_list,weight_func_1 ,cc_parameters, road = BFFA_parameters[:]
    # step 1: generate N initial fireflies in the search space, and evaluate their goodnes, the initalization gurantees feasability 
    firefly_population =  population.initialize_population(population_size, solution_size,  main_cars_list ,ramp_cars_list,road, cc_parameters)
    fitness_list = population.calc_fitness_list(firefly_population, weight_func_1, main_cars_list, ramp_cars_list, cc_parameters, road)

    #velocity
    v = []

    best_fitness_list = []
    #best_solution_list = []

    best_solution_overall = None
    best_fitness_overall = 0

    for t in range(num_of_iteration) :
        
        f_max = max(fitness_list) #maximum objective value so far
        non_dominated_fireflies =[]
        #Step 2: Update the jump probability
        jump_probabiliry = 0.1 - (0.09*( t / num_of_iteration ))

        #step 3:get attractivnes from each individual and the other
        for individual1 in range(population_size):  
            attractiveness_list = []  
            for individual2 in range(individual1, population_size):
                #get atrractivness and append it to the list
                attractiveness = population.eval_attractiveness(firefly_population[individual1], firefly_population[individual2],f_max,main_cars_list,ramp_cars_list,weight_func_1,cc_parameters,road) 
                attractiveness_list.append(attractiveness)
            
            
            sorted_firefly_population_attractiveness = sorted(firefly_population[individual1:population_size], key = lambda x:  - attractiveness_list[firefly_population[individual1:population_size].index(x)])

            #in our case of rcBFFA take the first one only
            #list of most attractive to individual1 and previous individual1 s
            non_dominated_fireflies.append(sorted_firefly_population_attractiveness[0])

            #choose a random attractiv firefly
            attractive_firefly_index = random.randint(0,len(non_dominated_fireflies)-1)
            attractive_firfly = non_dominated_fireflies[attractive_firefly_index]

            #you can get it from the already calculaed list or calculate it again
            attractiveness = population.eval_attractiveness(firefly_population[individual1], attractive_firfly, f_max,main_cars_list,ramp_cars_list,weight_func_1,cc_parameters,road)

            #v is the new position (velocity) of the solution  and it is the binary list
            v = firefly_population[individual1]
            #keep looping until it is feasabilie 
            feasibility = False
            while(not feasibility):
                #for each attaractive fire fly update velocity
                for index in range(len(attractive_firfly)):
                    rand1 = random.randint(0,1)
                    rand2 = random.randint(0,1)
                    #stay the same
                    if attractiveness > rand2:
                        v[index] = attractive_firfly[index]

                    if jump_probabiliry > rand1:
                        firefly_population[individual1][index] = 1 - v[index]
                    else:
                        firefly_population[individual1][index] =  v[index]
                feasibility  = sequence.check_feasibility(firefly_population[individual1], road, cc_parameters, main_cars_list, ramp_cars_list)
                #print("feasibility", feasibility)

            fitness_list = population.calc_fitness_list(firefly_population, weight_func_1, main_cars_list, ramp_cars_list, cc_parameters, road)
            sorted_firefly_population= sorted(firefly_population, key = lambda x:  - fitness_list[firefly_population.index(x)])

        best_solution_in_generation = sorted_firefly_population[0]
        #best_solution_list.append(best_solution_in_generation)

        best_fitness_in_generation = fitness_list[firefly_population.index(best_solution_in_generation)]
        best_fitness_list.append(best_fitness_in_generation)


        if best_fitness_in_generation > best_fitness_overall:
            best_fitness_overall = best_fitness_in_generation
            best_solution_overall = best_solution_in_generation


        
    
    
    return range(num_of_iteration), best_fitness_list, best_solution_overall, best_fitness_overall
                   

