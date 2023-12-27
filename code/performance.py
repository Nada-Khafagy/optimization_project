import matplotlib.pyplot as plt
import time
import SA
import math


def plot_fitness_against_progress(x, y, algo_name, x_label, y_label):
    plt.plot(x,y)
    # Add labels and a legend
    plt.ylim(0, 1)
    plt.xlabel(x_label, fontsize=16)
    plt.ylabel(y_label, fontsize=16)
    plt.title(algo_name, fontsize=16)
    if(algo_name == 'Simulated Annealing Algorithm'):
        plt.gca().invert_xaxis()
    plt.grid(True)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()

def get_avg_running_time(algo, algo_parameters, iterations_num):
    run_time_list = []
    for  _ in range(iterations_num):
        start_time = time.time()
        [x, y, best_solution,best_fitness] = algo(algo_parameters) 
        end_time = time.time() 
        running_time = end_time - start_time
        run_time_list.append(running_time)   
    avg_runing_time = sum(run_time_list)/len(run_time_list)
    algo_name = str(algo)
    algo_name = (algo_name[10:algo_name.find(' ',10)])

    print(f"Average {algo_name} excution time:  {avg_runing_time} seconds")
    return avg_runing_time

def compare_avg_runing_time(func,func_paramters, runs_num ):
    avg_runing_time_list = []
    for algos, algos_paramters in zip(func,func_paramters): 
        avg_time = get_avg_running_time(algos, algos_paramters, runs_num)
        avg_runing_time_list.append(avg_time)
    
    return avg_runing_time_list

#for now it is limited to 6
def compare_fitness(algo_list, algo_paramters_list, iterations_num):
    colors = ['r','b','y','k','g','c', 'm']
    for algo,algp_parameters,coluor in zip(algo_list, algo_paramters_list, colors):
        [x,y,best_sol, best_fitness] = algo(algp_parameters)
        algo_name = str(algo)
        algo_name = (algo_name[10:algo_name.find(' ',10)])
        plt.plot(range(1,iterations_num+1), y, label=algo_name, color=coluor, linewidth=2)  # Plot fitness
        if(algo_name == SA.simulated_annealing):
            plt.gca().invert_xaxis()

    plt.ylim(0, 1)
    plt.xlabel("Progress", fontsize=16)
    plt.ylabel("Fitness", fontsize=16)
    plt.legend()
    plt.title("Comparison between different algorithms", fontsize=16)     
    plt.grid(True)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()

#getting the worst means getting the worst outcome of this algorithim, since we outcome the best solution in all generation we will compare this outcome
def get_worst(algo, algo_parameters, iterations_num):
    worst_fitness_overall = 1
    worst_solution_overall = []
    for _ in range(iterations_num):
         [x, y, best_solution, best_fitness] = algo(algo_parameters)
         if(best_solution < worst_fitness_overall):
             worst_fitness_overall = best_fitness
             worst_solution_overall = best_solution
    algo_name = str(algo)
    algo_name = (algo_name[10:algo_name.find(' ',10)])
    print(f"Worst {algo_name} solution:{worst_solution_overall} ")
    print(f"Worst {algo_name} fitness: {worst_fitness_overall}" )
    return worst_solution_overall, worst_fitness_overall 

def get_best(algo, algo_parameters, iterations_num):
    best_fitness_overall = 0
    best_solution_overall = []
    for _ in range(iterations_num):
         [x, y, best_solution, best_fitness] = algo(algo_parameters)
         if( best_fitness > best_fitness_overall):
             best_fitness_overall = best_fitness
             best_solution_overall = best_solution
    #print data
    algo_name = str(algo)
    algo_name = (algo_name[10:algo_name.find(' ',10)])
    print(f"Best {algo_name} solution:{best_solution_overall} ")
    print(f"Best {algo_name} fitness: {best_fitness_overall}" )
    return best_solution_overall, best_fitness_overall 

#why you ask? so it can get all these info in the same loop ..
def evaluate_performance(algo, algo_parameters, iterations_num):
    best_fitness_overall = 0
    best_solution_overall = []
    worst_fitness_overall = 1
    worst_solution_overall = []
    run_time_list = []
    avg_fitness = 0
    fitness_sum = 0
    for  _ in range(iterations_num):
        start_time = time.time()
        [x, y, best_solution, best_fitness] = algo(algo_parameters) 
        if( best_fitness > best_fitness_overall):
            best_fitness_overall = best_fitness
            best_solution_overall = best_solution
        if(best_fitness < worst_fitness_overall):
             worst_fitness_overall = best_fitness
             worst_solution_overall = best_solution   
        end_time = time.time() 
        running_time = end_time - start_time
        run_time_list.append(running_time)      
        fitness_sum += best_fitness  
    avg_runing_time = sum(run_time_list) / len(run_time_list)
    avg_fitness = fitness_sum / iterations_num

    dev = 0
    for _ in range(iterations_num):
        [x, y, best_solution, best_fitness] = algo(algo_parameters) 
        dev += (avg_fitness - best_fitness)**2
    standard_dev = math.sqrt(dev) / iterations_num

    coefficient_of_variation = standard_dev / avg_fitness
    #print data
    algo_name = str(algo)
    algo_name = (algo_name[10:algo_name.find(' ',10)])
    print(f"Best {algo_name} solution in {iterations_num} runs :{best_solution_overall} ")
    print(f"Best {algo_name} fitness in {iterations_num} runs : {best_fitness_overall}" )
    print(f"Worst {algo_name} solution in {iterations_num} runs :{worst_solution_overall} ")
    print(f"Worst {algo_name} fitness in {iterations_num} runs : {worst_fitness_overall}" )
    print(f"Average {algo_name} excution time in {iterations_num} runs :  {avg_runing_time} seconds")
    print(f"Average {algo_name} fitness in {iterations_num} runs : {avg_fitness} ")
    print(f"Standard deviation of {algo_name} in {iterations_num} runs : {standard_dev} ")
    print(f"coefficient of variation of {algo_name} in {iterations_num} runs : {coefficient_of_variation} ")

    return best_solution_overall, best_fitness_overall, worst_solution_overall, worst_fitness_overall, avg_runing_time, avg_fitness
    
def get_average_fitness(algo, algo_parameters, iterations_num):
    avg_fitness = 0
    sum = 0
    for _ in range(iterations_num):
        [x, y, best_solution, best_fitness] = algo(algo_parameters) 
        sum += best_fitness   
    avg_fitness = sum / iterations_num
    return avg_fitness

def get_standard_deviation(algo, algo_parameters, iterations_num):
    avg_fitness = get_average_fitness(algo, algo_parameters, iterations_num)
    dev = 0
    for _ in range(iterations_num):
        [x, y, best_solution, best_fitness] = algo(algo_parameters) 
        dev += (avg_fitness - best_fitness)**2
    standard_dev = math.sqrt(dev) / iterations_num

    return standard_dev
    