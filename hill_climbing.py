'''
Note that it actually 'descend', to minimise fitness value.
'''

import ast
import astor
import sys
import random
from trace import Trace

INT_MAX = 3000

INT_MIN = 0

def normalize(n):
  alpha = 0.001

  return 1.0 - (1 + alpha)**(-n)

class HillClimbing():
    def __init__(self, target_function, AST, nodes_on_path):
        self.function_name = target_function['name']
        self.args_count = target_function['args_count']

        self.functionDef_source = compile(
            AST, '', 'exec')

        self.nodes_on_path = nodes_on_path

    def _make_function_call(self, args):
        source = '{func}('.format(func=self.function_name)

        for arg in args:
            source += '{arg}, '.format(arg=arg)

        source += 'trace)'

        return source

    def _generate_random_integers(self, count):
        args = []
        for i in range(count):
            integer = random.randint(INT_MIN, INT_MAX)
            args.append(integer)

        return args

    def _calculate_fitness_value(self, args):
        trace = Trace()

        exec(self.functionDef_source, locals())

        eval(self._make_function_call(args))

        executed_branches = trace.get_executed_branches()

        approach_level = 0
        for branch_num, branch_type in self.nodes_on_path:
            for num, result, distance_to_alternative in executed_branches:
                if branch_num == num:
                    if approach_level == 0 and branch_type == result:
                        return 0

                if branch_type != result:
                    return normalize(distance_to_alternative) + approach_level

            approach_level += 1


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
        fitness = self._calculate_fitness_value(args)

        while True:
            if fitness == 0:
                return args, fitness

            else:
                neighbors = self._find_neighbors(args)
                new_args = []
                for args_candidate in neighbors:
                    fitness_neighbor = self._calculate_fitness_value(args_candidate)

                    if fitness_neighbor < fitness:
                        new_args.append((args_candidate, fitness_neighbor))
                        break

                if len(new_args) == 0:
                    return args, fitness

                args = new_args[0][0]
                fitness = new_args[0][1]

    def minimise(self):
        initial_args = self._generate_random_integers(self.args_count)

        minimised_args, fitness_value = self.do_hill_descending(initial_args)

        return (minimised_args, fitness_value)
