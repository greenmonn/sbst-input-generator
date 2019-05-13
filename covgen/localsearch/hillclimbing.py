'''
Note that it actually 'descend', to minimise fitness value.
'''

import sys
import random

import logging


class HillClimbing():
    def __init__(self, fitness_calculator, retry_count=100, int_min=0, int_max=3000):
        self.fitness = fitness_calculator
        self.retry_count = retry_count

        self.int_min = int_min
        self.int_max = int_max

    def _generate_random_integers(self, count):
        args = []
        for i in range(count):
            integer = random.randint(self.int_min, self.int_max)
            args.append(integer)

        return args

    def _find_neighbors(self, args):
        neighbors = []
        for i in range(len(args)):
            neighbor1 = args[:]
            neighbor1[i] = args[i] + 1
            neighbors.append(neighbor1)

            neighbor2 = args[:]
            neighbor2[i] = args[i] - 1
            neighbors.append(neighbor2)

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
                
                logging.debug((args, fitness))

    def minimise(self):
        minimised_args = []
        fitness_value = 0

        for i in range(self.retry_count):
            initial_args = self._generate_random_integers(
                self.fitness.get_args_count())

            minimised_args, fitness_value = self.do_hill_descending(
                initial_args)

            if fitness_value == 0:
                break

        return (minimised_args, fitness_value)
