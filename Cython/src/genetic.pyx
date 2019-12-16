import numpy as np
import random
import os
if 'AI' in os.getcwd():
    from src.utils import *
else:
    from AI2019.src.utils import *

from src.constructive_algorithms import *
from src.local_search import *

class Genetic:

    @staticmethod
    def gen(solution, instance, populationSize=30, mutationRate = 0.015,
            tournamentSize = 5, elitism = True):
        pop = Population(instance, populationSize, True)

        # TODO after initial testing chenge to time based and not 100 runs
        for i in range(0, 10):
            print(pop.getBest().getFitness())
            pop = Genetic.evolve(pop, instance, mutationRate, elitism)

        best = pop.getBest().solution
        #improved = TwoOpt.loop2opt(best, instance)
        sol = np.append(best, best[0])
        improved = TwoOpt.loop2opt(sol, instance)
        #improved2 = TwoDotFiveOpt.loop2dot5opt(sol, instance)
        return improved
        #return sol

    @staticmethod
    def evolve(population, instance, mutationRate, elitism):
        newPopulation = Population(instance, population.size, False)

        elitismN = 0
        if elitism:
            best = population.getBest()
            #improved = TwoOpt.loop2opt(best.solution, instance)
            #best.solution = improved
            #print("elite fitness: {}".format(best.getFitness()))
            #newPopulation.tours.append(best)
            newBest = Tour(instance)
            #newBest.solution = np.array(improved)
            newBest.solution = np.array(best.solution)
            newPopulation.tours.append(newBest)
            #newPopulation.tours.append(population.getBest())
            elitismN = 1

        """
        for i in range(elitismN, newPopulation.size):
            # look if we want TSelection as function or Population method
            parent1 = Genetic.TSelection(instance, population)
            parent2 = Genetic.TSelection(instance, population)
            #parent1.solution = TwoOpt.loop2opt(parent1.solution, instance)
            #parent2.solution = TwoOpt.loop2opt(parent2.solution, instance)

            newPopulation.tours.append(Genetic.crossover3(parent1, parent2,
                    instance))
            """
        """
            child = Genetic.crossover3(parent1, parent2, instance)
            child.solution = TwoOpt.loop2opt(child.solution, instance)
            newPopulation.tours.append(child)
            """
        """

        for i in range(elitismN, population.size):
            #Genetic.mutate(newPopulation.tours[i], mutationRate)
            #print("Fitness before mutation: {}".format(population.tours[i].getFitness()))

            # This is the base one
            #Genetic.mutate(population.tours[i], mutationRate)

            #print("Fitness after mutation: {}".format(population.tours[i].getFitness()))
            #newPopulation.tours[i].solution = TwoOpt.loop2opt(newPopulation.tours[i].solution, instance)
            """
        """
            newPopulation.tours.append(Genetic.mutate(population.tours[i],
                mutationRate))
            """
        """
            newPopulation.tours[i] = Genetic.mutate(newPopulation.tours[i],
                mutationRate)
            newPopulation.tours[i].solution = TwoOpt.loop2opt(newPopulation.tours[i].solution, instance)
        """

        for i in range(elitismN, newPopulation.size):
            parent1 = Genetic.TSelection(instance, population)
            parent2 = Genetic.TSelection(instance, population)
            child = Genetic.crossover3(parent1, parent2, instance)
            childM = Genetic.mutate(child, mutationRate)
            childM.solution = TwoOpt.loop2opt(childM.solution, instance, 3)
            newPopulation.tours.append(childM)


        #print("best fitness at the end: {}".format(newPopulation.getBest().getFitness()))
        return newPopulation

    @staticmethod
    def crossover(parent1, parent2, instance):
        child = Tour(instance)
        tempSol = []
        lenPar1Sol = len(parent1.solution)
        for i in range(0, lenPar1Sol):
            #child.solution.append(None)
            tempSol.append(None)
        child.solution = np.array(tempSol)

        startPos = random.randrange(0, lenPar1Sol)
        endPos = random.randrange(0, lenPar1Sol)

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
        #print(parent1.getFitness(), parent2.getFitness(), child.getFitness())
        return child

    #This is from the paper of 7 cities
    @staticmethod
    def crossover2(parent1, parent2, instance):
        child = Tour(instance)
        tempSol = []
        lenPar1Sol = len(parent1.solution)
        for i in range(0, lenPar1Sol):
            #child.solution.append(None)
            tempSol.append(None)
        child.solution = np.array(tempSol)

        nP1 = parent1.solution[0]
        index = None
        for i in range(0, lenPar1Sol):
            if parent2.solution[i] == nP1:
                index = i
                break

        distP1 = valueDist(nP1, parent1.solution[1])
        distP2 = valueDist(parent2.solution[index], parent2.solution[(index +
            1) % lenPar1Sol])

        choice = None
        if distP1 < distP2:
            choice = parent1.solution[1]
        else:
            choice = parent2.solution[(index + 1) % lenPar1Sol]

        # TODO
        # add choice
        # add rest
        # chose if we want to use the modulo or shift everything in the
        # numeration in order to have both start from the first node
        # (I think it's still a modulo or something)

    #This is the partially mapped crossover
    @staticmethod
    def crossover3(parent1, parent2, instance):
        child = Tour(instance) #here tour calls a NN and I don't want that
        indices = {}
        length = len(parent1.solution)
        cross1 = random.randrange(0, length)
        cross2 = random.randrange(0, length)
        # copy from first parent
        temp = np.array(parent1.solution)
        for i in range(0, length):
            indices[temp[i]] = i
        
        if cross1 > cross2:
            cross1, cross2 = cross2, cross1

        for i in range(cross1, cross2 + 1): #TODO check if the + 1 is right
            value = parent2.solution[i]
            t = temp[indices[value]]
            temp[indices[value]] = temp[i]
            temp[i] = t
            t = indices[temp[indices[value]]]
            indices[temp[indices[value]]] = indices[temp[i]]
            indices[temp[i]] = t

        child.solution = np.array(temp)
        #print(parent1.getFitness(), parent2.getFitness(), child.getFitness())
        """
        if (child.getFitness() > parent1.getFitness()) and (child.getFitness()
                > parent2.getFitness()):
            print("Evolution! Child fitness: {}".format(child.getFitness()))
        """
        return child


    @staticmethod
    def mutate(individual, mutationRate):
        for city1 in range(0, len(individual.solution)):
            if (random.random() < mutationRate):
                city2 = random.randrange(0, len(individual.solution))
                while city2 == city1:
                    city2 = random.randrange(0, len(individual.solution))
                individual.solution[city1], individual.solution[city2] = individual.solution[city2], individual.solution[city1]
        # added for the version with only mutate
        return individual
                

    @staticmethod
    def TSelection(instance, population):
        tournament = Population(instance, 5, False)
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
                #self.tours.append(Tour(self.instance).generateIndividual())
                t = Tour(self.instance)
                t.generateIndividual()
                self.tours.append(t)

    def getBest(self):
        best = self.tours[0]
        bestF = best.getFitness()
        for i in range(1, self.size):
            #print(self.tours[i].solution)
            #print(self.tours[i].getFitness())
            if bestF < self.tours[i].getFitness():
                best = self.tours[i]
                bestF = best.getFitness()
        return best


class Tour:

    def __init__(self, instance):
        self.fitness = 0
        self.distance = 0
        self.instance = instance
        self.solution = None
        """
        self.solution = nearest_neighbor.nn(self.instance, random.randrange(0,
            self.instance.nPoints))[:-1]
        """
        #print("len of solution at Tour initialization: {}".format(len(self.solution)))
        #print("solution at Tour initialization: {}".format(self.solution))
        
        #self.solution = random_initialier.random_method(self.instance)

    def generateIndividual(self):
        #is this the correct/efficent way of doing it?
        #self.solution = random_initialier.random_method(self.instance)

        #let's try with nearest neighbour
        self.solution = nearest_neighbor.nn(self.instance, random.randrange(0,
            self.instance.nPoints))[:-1]

    def getFitness(self):
        #if self.fitness == 0:
            #is this the correct/efficent way of doing it? (see method below)
        self.fitness = 1 / self.evaluate_sol()
            #print("evaluate_sol(): {}".format(self.evaluate_sol()))
        return self.fitness

    def evaluate_sol(self):
        #print("tour.solution: {}".format(self.solution)) #this is right
        total_length = 0
        solutionT = np.append(self.solution, self.solution[0])

        starting_node = solutionT[0]
        index = 1
        while starting_node == None:
            starting_node = solutionT[index]
            index += 1

        #print("starting_node: {}".format(starting_node))
        from_node = starting_node
        for node in solutionT[1:]:
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
