import numpy as np
import os
if 'AI' in os.getcwd():
    from src.utils import *
else:
    from AI2019.src.utils import *

from src.local_search import *
from time import time as t
import random


class Simulated_Annealing:

    @staticmethod
    def sa(solution, instance, constant_temperature=0.45, iterations_for_each_temp=10):

        # initial setup
        temperature = instance.best_sol / np.sqrt(instance.nPoints)
        current_sol = np.array(solution)
        current_len = compute_lenght(solution, instance.dist_matrix)
        best_sol = np.array(solution)
        best_len = current_len

        count = 0

        # main loop
        while temperature > 0.001:
            count += 1
            for it in range(iterations_for_each_temp):
                next_sol, delta_E = Simulated_Annealing.random_sol_from_neig(current_sol, instance)
                #next_sol = TwoOpt.loop2opt(next_sol, instance)
                next_sol = Iterated_Local_Search.double_bridge(next_sol)
                if delta_E < 0:
                    current_sol = next_sol
                    current_len += delta_E
                    if current_len < best_len:
                        best_sol = current_sol
                        best_len = current_len
                else:
                    r = np.random.uniform(0, 1)
                    if r < np.exp(- delta_E / temperature):
                        current_sol = next_sol
                        current_len += delta_E

            temperature *= constant_temperature

        print(count)
        return best_sol.tolist()

    @staticmethod
    def random_sol_from_neig(solution, instance):
        i, j = np.random.choice(np.arange(1, len(solution) - 1), 2, replace=False)
        i, j = np.sort([i, j])
        return Simulated_Annealing.swap2opt(solution, i, j), Simulated_Annealing.gain(i, j, solution, instance.dist_matrix)

    @staticmethod
    def random_sol_from_neig2(solution, instance):
        i, j = np.random.choice(np.arange(1, len(solution) - 1), 2, replace=False)
        i, j = np.sort([i, j])
        return Simulated_Annealing.swap2opt(solution, i, j)

    @staticmethod
    def swap2opt(tsp_sequence, i, j):
        new_tsp_sequence = np.copy(tsp_sequence)
        new_tsp_sequence[i:j + 1] = np.flip(tsp_sequence[i:j + 1], axis=0)  # flip or swap ?
        return new_tsp_sequence

    @staticmethod
    def gain(i, j, tsp_sequence, matrix_dist):
        old_link_len = (matrix_dist[tsp_sequence[i], tsp_sequence[i - 1]] + matrix_dist[
            tsp_sequence[j], tsp_sequence[j + 1]])
        changed_links_len = (matrix_dist[tsp_sequence[j], tsp_sequence[i - 1]] + matrix_dist[
            tsp_sequence[i], tsp_sequence[j + 1]])
        return - old_link_len + changed_links_len


class Iterated_Local_Search:

    def __call__(self):
        pass

    @staticmethod
    def ils(solution, instance, constant_temperature=0.95,
            iterations_for_each_temp=1):
        start = t()
        temperature = instance.best_sol / np.sqrt(instance.nPoints)
        current_sol = np.array(solution)
        current_sol = TwoOpt.loop2opt(current_sol, instance)
        current_len = compute_lenght(current_sol, instance.dist_matrix)
        best_sol = current_sol
        best_len = current_len
        while temperature > 0.001 and t() - start < 150:
            #print(temperature)
            for i in range(iterations_for_each_temp):
                if t() - start > 150:
                    break
                mutated_sol = Simulated_Annealing.random_sol_from_neig2(current_sol, instance)
                #mstart = t()
                #mutated_sol = Iterated_Local_Search.double_bridge(current_sol)
                #opt_sol = mutated_sol
                #mend = t()
                opt_sol = TwoOpt.loop2opt(mutated_sol, instance)
                #opt_sol = TwoDotFiveOpt.loop2dot5opt(mutated_sol, instance, 3)
                #optEnd = t()
                #print(mend - mstart, optEnd - mend)
                #delta_E = Iterated_Local_Search.evaluate_sol(opt_sol, instance) - best_len
                delta_E = compute_lenght(opt_sol, instance.dist_matrix) - best_len
                if delta_E < 0:
                    #print("Improvement")
                    current_sol = opt_sol
                    current_len += delta_E
                    if current_len < best_len:
                        best_sol = current_sol
                        best_len = current_len
                else:
                    r = np.random.uniform(0, 1)
                    if r < np.exp(- delta_E / temperature):
                        current_sol = opt_sol
                        current_len += delta_E

            temperature *= constant_temperature
        return best_sol

    @staticmethod
    def evaluate_sol(solution, instance):
        total_length = 0
        solutionT = np.append(solution, solution[0])

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
                total_length += instance.dist_matrix[from_node, node]
                #print("total_length: {}".format(total_length))
                from_node = node

        #print("total length: " + str(total_length))
        return total_length

    @staticmethod
    def double_bridge(solution):
        solution = solution[:-1]
        pos1 = 1 + random.randrange(0, round(len(solution) / 4))
        pos2 = pos1 + random.randrange(0, round(len(solution) / 4))
        pos3 = pos2 + random.randrange(0, round(len(solution) / 4))
        #t = solution[:pos1] + solution[pos3:]
        p1 = np.concatenate((solution[:pos1],solution[pos3:]))
        p2 = np.concatenate((solution[pos2:pos3], solution[pos1:pos2]))
        res = np.concatenate((p1, p2))
        #print(res)
        resA = np.append(res, res[0])
        #print(resA)
        return resA
