import numpy as np
class Particle:
    def __init__(self, intial_solution):
        self.solution = intial_solution 
        self.position = np.array(self.solution) #get position vector from solution list
        zeros = len(intial_solution)*[0.1]
        self.velocity = np.zeros(len(intial_solution)) #zero velocity
        self.fitness = 0
        #personal best
        self.Pbest_position = self.position
        self.Pbest_fitness = self.fitness
        #solution is a binary list
        self.Pbest_solution = self.solution

        #global best
        self.Nbest_position = self.position
        self.Nbest_fitness = self.fitness
        self.Nbest_solution = self.solution