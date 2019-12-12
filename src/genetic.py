import numpy as np
import random
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
            # look if we want TSelection as function or Population method
            # TODO implement TSelection
            parent1 = TSelection(population)
            parent2 = TSelection(population)

            newPopulation.tour[i] =  cross(parent1, parent2)

        for i in range(elitismN, newPopulation.size):
            mutate(newPopulation.tour[i])

        return newPopulation

    def crossover(parent1, parent2, instance):
        child = Tour(instance)

        startPos = random.randrange(0, len(parent1.solution))
        endPos = random.randrange(0, len(parent1.solution))

        for i in range(0, len(child.solution)):
            if startPos < endPos and i > startPos and i < endPos:
                child.solution[i] = parent1.solution[i]
            elif startPos > endPos:
                if not (i < startPos && i > endPos):
                    child.solution[i] = parent1.solution[i]

        for i in range(0, len(parent2.solution)):
            # super bottleneck in my opinion, in conjunction with the search
            # for the first available slot
            if not child.containsNode(parent2.solution[i]):
                for j in range(0, len(child.solution)):
                    # this assumes fixex arrays created with None as in Java/C
                    # TODO find solution (initialize or other)
                    if child.solution[j] == None:
                        child.solution[j] = parent2.solution[i]
                        break

        return child

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

    #TODO check if it's right
    def containsNode(self, node):
        for i in range(0, len(self.solution)):
            if self.solution[i] == node:
                return True
        return False
