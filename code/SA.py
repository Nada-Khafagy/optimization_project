import numpy as np
import objective_func
import randomize_sequence


def acceptance_probability(f1, f2, temperature):
    delta_f = f2 - f1
    # Compute the acceptance probability based on the current and new objective functions values
    if f2 > f1:
        return 1
    else:
        P = np.exp((-delta_f) / temperature)
        return P

def simulated_annealing(initial_temperature, cooling_rate, num_iterations):
    sequence_car_info1 = randomize_sequence.randomize_sequence()
    current_objective = objective_func.objective_func(w1, r, rl, sequence_car_info1, min_v,max_v)
    current_solution = sequence_car_info1
    best_solution = current_solution
    best_objective = current_objective
    temperature = initial_temperature

    for i in range(num_iterations):
        sequence_car_info2 = randomize_sequence.randomize_sequence()
        new_objective = objective_func.objective_func(w1, r, rl, sequence_car_info2, min_v,max_v)
        acceptance_prob = acceptance_probability(current_objective, new_objective, temperature)
        
        if acceptance_prob > np.random.rand():
            current_solution = sequence_car_info2
            current_objective = new_objective
        
        if current_objective > best_objective:
            best_solution = current_solution
            best_objective = current_objective
        
        temperature *= cooling_rate

    return best_solution, best_objective

# Example usage
initial_temperature = 100.0
cooling_rate = 0.95
num_iterations = 1000

best_solution, best_objective = simulated_annealing(initial_temperature, cooling_rate, num_iterations)
print("Best solution:", best_solution)
print("Best objective:", best_objective)