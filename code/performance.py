import matplotlib.pyplot as plt
import time
import SA


def plot_fitness_against_progress(x, y, algo_name, x_label, y_label):
    plt.plot(x,y)
    # Add labels and a legend
    plt.ylim(0, 1)
    plt.xlabel(x_label, fontsize=14)
    plt.ylabel(y_label, fontsize=14)
    plt.title(algo_name, fontsize=16)
    if(algo_name == 'Simulated Annealing Algorithm'):
        plt.gca().invert_xaxis()
    plt.grid(True)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()

def get_avg_running_time(func, func_paramters, runs_num):
    run_time_list = []
    for  _ in range(runs_num):
        start_time = time.time()
        [x, y, best_solution,best_objective] = func(func_paramters) 
        end_time = time.time() 
        running_time = end_time - start_time
        run_time_list.append(running_time)
    
    avg_runing_time = sum(run_time_list)/len(run_time_list)
    return avg_runing_time

def compare_avg_runing_time(func,func_paramters, runs_num ):
    avg_runing_time_list = []
    for algos, algos_paramters in zip(func,func_paramters): 
        avg_time = get_avg_running_time(algos, algos_paramters, runs_num)
        avg_runing_time_list.append(avg_time)
    return avg_runing_time_list

    
def compare_fitness(func,func_paramters, iterations_num):
    for algo,algp_parameters in zip(func, func_paramters):
        [x,y,best_sol, best_fitness] = algo(algp_parameters)
        algo_name = str(algo)
        algo_name = (algo_name[10:algo_name.find(' ',10)])
        plt.plot(range(1,iterations_num+1), y, label=algo_name, color='r', linewidth=2)  # Plot fitness
        if(algo_name == SA.simulated_annealing):
            plt.gca().invert_xaxis()
    plt.ylim(0, 1)
    plt.xlabel("progress", fontsize=14)
    plt.ylabel("fitness", fontsize=14)
    plt.title("comparison between different algorithims", fontsize=16)     
    plt.grid(True)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()


    