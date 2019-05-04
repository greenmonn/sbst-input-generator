import random
import sys
import ast
import astor

from trace import Trace
from parse_ast import ASTParser

INT_MAX = sys.maxsize

INT_MIN = -sys.maxsize-1


def generate_random_integers(count):
    args = []
    for i in range(count):
        integer = random.randint(INT_MIN, INT_MAX)
        args.append(integer)

    return args


class InputGenerator():
    def __init__(self, parser):
        parser.insert_hooks()
        target_function = parser.get_target_function()
        parser.print_predicates_tree()

        self.parser = parser

        self.args_count = target_function['args_count']
        self.node = target_function['node']
        self.func_name = target_function['name']

    def _make_function_call(self, args):
        source = '{func}('.format(func=self.func_name)

        for arg in args:
            source += '{arg}, '.format(arg=arg)
        
        source += 'trace)'

        return source

    def generate_input(self, target_branch_id):
        args = generate_random_integers(self.args_count)

        trace = Trace()

        function_def = compile(ast.Module([self.node]), '', 'exec')
        exec(function_def)

        eval(self._make_function_call(args))

        executed_branches = trace.get_executed_branches()

        nodes_on_path = self.parser.get_nodes_on_path(target_branch_id)

        fitness_value = self.calculate_fitness_value(executed_branches, nodes_on_path)

        if fitness_value == 0:
            return args

        else:
            neighbors = self._find_neighbors(args)
            new_fitness_value = 10000

            for new_args in neighbors:
                trace = Trace()
                
                eval(self._make_function_call(new_args))

                executed_branches = trace.get_executed_branches()

                nodes_on_path = self.parser.get_nodes_on_path(target_branch_id)

                new_fitness_value = self.calculate_fitness_value(
                executed_branches, nodes_on_path)

                if new_fitness_value < fitness_value:
                    args = new_args


    def calculate_fitness_value(self, executed_branches, nodes_on_path):
        approach_level = 0
        for branch_num, branch_type in nodes_on_path:
            for num, result, distance_to_alternative in executed_branches:
                if branch_num == num:
                    if approach_level == 0 and branch_type == result:
                        return 0

                if branch_type != result:
                    return distance_to_alternative + approach_level

            approach_level += 1
        
        return -1
        

    def generate_all_inputs(self):
        pass
        # target function의 모든 branch들에 대해서 (1T, 1F, ...)

        # generate_input을 call한다.

        # branch id에 대해 generate된 input(tuple)을 출력


parser = ASTParser('target/triangle.py')

generator = InputGenerator(parser)

generator.generate_input('1T')
