import numpy as np
class Particle:
    def __init__(self, solution_size):
        self.position = np.random.randint(2, size = solution_size)  # Initialize binary positions (0 or 1)
        self.velocity = np.zeros(shape = solution_size)
        self.solution = []  # Initialize the solution attribute
        self.fitness = 0
        self.best_position = self.position
        self.best_fitness = self.cost