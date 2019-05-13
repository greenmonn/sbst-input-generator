import sys
import copy
import operator

import covgen.types.branchutil as branchutil

from covgen.parser.ast_parser import ASTParser

from covgen.localsearch.fitnesscalc import FitnessCalculator
from covgen.localsearch.hillclimbing import HillClimbing
from covgen.localsearch.avm import AVM


class NoTargetFunctionException(Exception):
    """Exception raised when no target function is found with given name.

    Attributes:
        name -- function name given
        message -- explanation of the error
    """

    def __init__(self, name, message):
        self.name = name
        self.message = message


class InputGenerator():
    def __init__(self, file, function_name=None, method=None, retry=100, int_min=0, int_max=3000):
        parser = ASTParser(file)

        self.method = method
        self.retry_count = retry
        self.function_defs = parser.function_defs
        self.AST = parser.AST
        self.target_function = None

        if function_name is not None:
            try:
                self.set_target_function(function_name)

            except NoTargetFunctionException as err:
                print('{}: {}'.format(err.message, err.name))
                exit(1)

    def set_target_function(self, name):
        for f in self.function_defs:
            if f.name == name:
                target_function = copy.deepcopy(f)

                target_function.insert_hooks_on_predicates()
                self.target_function = target_function
                # self.target_function.branch_tree.print()
                return

        raise NoTargetFunctionException(
            name, 'Cannot find target function definition with given name')

    def print_branch_tree(self):
        if self.target_function is not None:
            self.target_function.branch_tree.print()

    def generate_input(self, target_branch_id):
        if self.target_function is None:
            print('Please set target function!')
            return

        fitness_calculator = FitnessCalculator(
            self.target_function, target_branch_id, self.AST)

        searcher = None
        if self.method == 'avm':
            searcher = AVM(fitness_calculator, self.retry_count)

        elif self.method == 'hillclimbing':
            searcher = HillClimbing(fitness_calculator, self.retry_count)

        else:
            # mix possible methods
            searcher = AVM(fitness_calculator, self.retry_count)
            minimised_args, fitness_value = searcher.minimise()

            if fitness_value == 0:
                return minimised_args

            else:
                searcher = HillClimbing(fitness_calculator, self.retry_count)

        minimised_args, fitness_value = searcher.minimise()

        if fitness_value == 0:
            return minimised_args

        else:
            return None

    def generate_all_inputs(self):
        next_target_functions = []
        all_inputs = {}

        if self.target_function is None:
            for f in self.function_defs:
                next_target_functions.append(f.name)

            self.set_target_function(next_target_functions.pop())

        while True:
            branch_tree = self.target_function.branch_tree

            branches = branch_tree.get_all_branches()

            inputs = {}

            for branch in branches:
                branch_id = branchutil.create_branch_id(branch)

                args = self.generate_input(branch_id)

                inputs[branch_id] = args

                parents = branch_tree.get_nodes_on_path(branch_id)[1:]

                for branch in parents:
                    parent_id = branchutil.create_branch_id(branch)

                    if inputs[parent_id] == None:
                        inputs[parent_id] = args

            all_inputs[self.target_function.name] = inputs

            if len(next_target_functions) == 0:
                break

            self.set_target_function(next_target_functions.pop())

        return all_inputs

    def generate_all_inputs_and_print(self):
        all_inputs = self.generate_all_inputs()

        for function_name, inputs in all_inputs.items():
            print('[{}]'.format(function_name))

            if len(inputs.items()) == 0:
                print('no branch detected')

            for branch_id, args in sorted(inputs.items(), key=branchutil.compare_branch_id):
                line = '{}:'.format(branch_id)
                if args is None:
                    line += ' -'
                else:
                    for arg in args:
                        line += ' {}'.format(arg)

                print(line)

            print('')


def print_help():
    print('Usage: python inputgenerator.py <target file location>')
    print(
        '       python inputgenerator.py <target file location> --function <target function name> --method <method name=avm or hillclimbing> --retry-count <retry_count> --int-min <minimum int> --int-max <maximum int>')
    print(
        '       python inputgenerator.py <target file location> -f <target function name> -m <method name=avm or hillclimbing> -r <retry_count>')


def execute():
    if len(sys.argv) < 2:
        print_help()
        exit(1)

    target_file = sys.argv[1]
    target_function = None
    search_method = None
    retry_count = 100
    int_min = -10000
    int_max = 10000

    index = 2
    while index + 1 < len(sys.argv):
        option = sys.argv[index]
        if option == '-f' or option == '--function':
            target_function = sys.argv[index+1]

        elif option == '-m' or option == '--method':
            search_method = sys.argv[index+1]

        elif option == '-r' or option == '--retry-count':
            retry_count = int(sys.argv[index+1])

        elif option == '--int-min':
            int_min = int(sys.argv[index+1])
        
        elif option == '--int-max':
            int_max = int(sys.argv[index+1])

        else:
            print('unknown option: {}'.format(option))
            print_help()
            exit(1)

        index = index + 2

    generator = InputGenerator(
        target_file, target_function, method=search_method, retry=retry_count)

    generator.generate_all_inputs_and_print()


if __name__ == "__main__":
    execute()
