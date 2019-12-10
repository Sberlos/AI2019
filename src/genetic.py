import numpy as np
import os
if 'AI' in os.getcwd():
    from src.utils import *
else:
    from AI2019.src.utils import *

class Genetic:

    @staticmethod
    def gen(solution, instance, population=100, mutationRate = 0.015,
            tournamentSize = 5, elitism = True):
        pass


class Population:

    def __init__(self, size, shouldInitialize):

    def getBest(self):
        best = self.tours[0]
        for i in range(1, self.size):
            if best.getFitness() < tours[i].getFitness():
                best = tours[i]
        return best


class Tour:

    def __init__(self, instance):
        self.fitness = 0
        self.distance = 0
        self.instance = instance
        self.solution = None

    def generateIndividual(self):
        #is this the correct/efficent way of doing it?
        self.solution = random_initialier.random_method(self.instance)

    def getFitness(self):
        if self.fitness == 0:
            #is this the correct/efficent way of doing it? (see method below)
            self.fitness = 1 / self.evaluate_sol()
        return self.fitness

    def evaluate_sol(self):
        total_length = 0
        starting_node = self.solution[0]
        from_node = starting_node
        for node in self.solution[1:]:
            total_length += self.instance.dist_matrix[from_node, node]
            from_node = node

        return total_length
