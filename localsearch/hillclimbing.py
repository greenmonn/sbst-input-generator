'''
Note that it actually 'descend', to minimise fitness value.
'''

import ast
import astor
import sys
import random
from covgen.trace.trace import Trace

INT_MAX = 3000
INT_MIN = 0

MAX_RETRY_COUNT = 10


class HillClimbing():
    def __init__(self, fitness_calculator):
        self.fitness = fitness_calculator

    def _generate_random_integers(self, count):
        args = []
        for i in range(count):
            integer = random.randint(INT_MIN, INT_MAX)
            args.append(integer)

        return args

    def _find_neighbors(self, args):
        neighbors = []
        for i in range(len(args)):
            neighbor = args[:]
            neighbor[i] = args[i] + 1
            neighbors.append(neighbor)

            neighbor[i] = args[i] - 1
            neighbors.append(neighbor)

        return neighbors

    def do_hill_descending(self, args):
        fitness = self.fitness.calculate(args)

        while True:
            if fitness == 0:
                return args, fitness

            else:
                neighbors = self._find_neighbors(args)
                new_args = []
                for args_candidate in neighbors:
                    fitness_neighbor = self.fitness.calculate(
                        args_candidate)

                    if fitness_neighbor < fitness:
                        new_args.append((args_candidate, fitness_neighbor))
                        break

                if len(new_args) == 0:
                    return args, fitness

                args = new_args[0][0]
                fitness = new_args[0][1]

    def minimise(self):
        minimised_args = []
        fitness_value = 0

        for i in range(MAX_RETRY_COUNT):
            initial_args = self._generate_random_integers(
                self.fitness.get_args_count())

            minimised_args, fitness_value = self.do_hill_descending(
                initial_args)

            if fitness_value == 0:
                break

        return (minimised_args, fitness_value)
