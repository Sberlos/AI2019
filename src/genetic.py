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

    def evolve(population, instance):
        newPopulation = Population(instance, population.size, False)

        elitismN = 0
        if elitism:
            newPopulation.tour[0] = population.getBest()
            elitismN = 1

        for i in range(elitismN, newPopulation.size):
            parent1 = TSelection(population)
            parent2 = TSelection(population)

            newPopulation.tour[i] =  cross(parent1, parent2)

        for i in range(elitismN, newPopulation.size):
            mutate(newPopulation.tour[i])

        return newPopulation

    def crossover(parent1, parent2, instance):
        child = Tour(instance)


class Population:

    def __init__(self, instance, size, shouldInitialize):
        self.instance = instance
        self.size = size
        self.shouldInitialize = shouldInitialize
        self.tours = Tour(self.instance)
        if shouldInitialize:
            for i in range(0, self.size):
                self.tours[i] = Tour(self.instance).generateIndividual()

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
