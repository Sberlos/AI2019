import numpy as np
import random
import os
if 'AI' in os.getcwd():
    from src.utils import *
else:
    from AI2019.src.utils import *

from src.constructive_algorithms import *

class Genetic:

    @staticmethod
    def gen(solution, instance, populationSize=100, mutationRate = 0.015,
            tournamentSize = 5, elitism = True):
        pop = Population(instance, populationSize, True)

        # TODO after initial testing chenge to time based and not 100 runs
        for i in range(0, 100):
            print(i) #crasha con i = 1
            pop = Genetic.evolve(pop, instance, mutationRate, elitism)

        return pop.getBest().solution

    @staticmethod
    def evolve(population, instance, mutationRate, elitism):
        newPopulation = Population(instance, population.size, False)

        elitismN = 0
        if elitism:
            newPopulation.tours.append(population.getBest())
            elitismN = 1

        for i in range(elitismN, newPopulation.size):
            # look if we want TSelection as function or Population method
            parent1 = Genetic.TSelection(instance, population)
            parent2 = Genetic.TSelection(instance, population)

            newPopulation.tours.append(Genetic.crossover(parent1, parent2,
                    instance))

        for i in range(elitismN, newPopulation.size):
            Genetic.mutate(newPopulation.tours[i], mutationRate)

        return newPopulation

    @staticmethod
    def crossover(parent1, parent2, instance):
        child = Tour(instance)
        tempSol = []
        for i in range(0, len(parent1.solution)):
            #child.solution.append(None)
            tempSol.append(None)
        child.solution = np.array(tempSol)

        startPos = random.randrange(0, len(parent1.solution))
        endPos = random.randrange(0, len(parent1.solution))

        for i in range(0, len(child.solution)):
            if startPos < endPos and i > startPos and i < endPos:
                child.solution[i] = parent1.solution[i]
            elif startPos > endPos:
                if not (i < startPos and i > endPos):
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

        #print(child)
        #print(child.solution)
        
        #This makes things "work" but it's wrong
        #return child.solution

        return child

    @staticmethod
    def mutate(individual, mutationRate):
        for city1 in range(0, len(individual.solution)):
            if (random.random() < mutationRate):
                city2 = random.randrange(0, len(individual.solution))
                individual.solution[city1], individual.solution[city2] = individual.solution[city2], individual.solution[city1]
        """
        #this "works" but it's wrong (it failes on other places)
        for city1 in range(0, len(individual)):
            if (random.random() < mutationRate):
                city2 = random.randrange(0, len(individual))
                individual[city1], individual[city2] = individual[city2], individual[city1]
        """

    @staticmethod
    def TSelection(instance, population):
        tournament = Population(instance, population.size, False)
        for i in range(0, population.size):
            tournament.tours.append(population.tours[random.randrange(0,
                population.size)])
        
        return tournament.getBest()
        

class Population:

    def __init__(self, instance, size, shouldInitialize):
        self.instance = instance
        self.size = size
        self.shouldInitialize = shouldInitialize
        #self.tours = Tour(self.instance)
        self.tours = []
        if shouldInitialize:
            for i in range(0, self.size):
                #self.tours[i] = Tour(self.instance).generateIndividual()
                #self.tours.append(Tour(self.instance).generateIndividual())
                #print(self.tours[i].solution)
                self.tours.append(Tour(self.instance))

    def getBest(self):
        #print(self.size)
        """
        for j in range(0, self.size):
            #print(j)
            #print(self.tours[j])
        """

        best = self.tours[0]
        #print(best)
        for i in range(1, self.size):
            #print(self.tours[i].solution)
            #print(self.tours[i].getFitness())
            if best.getFitness() < self.tours[i].getFitness():
                best = self.tours[i]
        return best


class Tour:

    def __init__(self, instance):
        self.fitness = 0
        self.distance = 0
        self.instance = instance
        #self.solution = None
        self.solution = nearest_neighbor.nn(self.instance, random.randrange(0,
            self.instance.nPoints))

    def generateIndividual(self):
        #is this the correct/efficent way of doing it?
        #self.solution = random_initialier.random_method(self.instance)

        #let's try with nearest neighbour
        self.solution = nearest_neighbor.nn(self.instance, random.randrange(0,
            self.instance.nPoints))

    def getFitness(self):
        if self.fitness == 0:
            #is this the correct/efficent way of doing it? (see method below)
            self.fitness = 1 / self.evaluate_sol()
            #print("evaluate_sol(): {}".format(self.evaluate_sol()))
        return self.fitness

    def evaluate_sol(self):
        #print("tour.solution: {}".format(self.solution)) #this is right
        total_length = 0

        starting_node = self.solution[0]
        index = 1
        while starting_node == None:
            starting_node = self.solution[index]
            index += 1

        #print("starting_node: {}".format(starting_node))
        from_node = starting_node
        for node in self.solution[1:]:
            if node != None:
                #print("node: {}".format(node))
                total_length += self.instance.dist_matrix[from_node, node]
                #print("total_length: {}".format(total_length))
                from_node = node

        #print("total length: " + str(total_length))
        return total_length

    def containsNode(self, node):
        for i in range(0, len(self.solution)):
            if self.solution[i] == node:
                return True
        return False
