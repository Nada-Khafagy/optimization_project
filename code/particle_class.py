import numpy as np
class Particle:
    def __init__(self, intial_position):
        self.position = intial_position
        self.velocity = 0.01 #near zero velocity
        self.solution = []  # Initialize the solution attribute
        self.fitness = 0
        self.Pbest_position = self.position
        self.Pbest_fitness = self.fitness
        self.Nbest_position = self.position
        self.Nbest_fitness = self.fitness