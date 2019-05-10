import sys
import copy
import operator

from covgen.parser.ast_parser import ASTParser

from covgen.localsearch.fitnesscalc import FitnessCalculator
from covgen.localsearch.hillclimbing import HillClimbing


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
    def __init__(self, file, function_name=None):
        parser = ASTParser(file)

        self.function_defs = parser.function_defs
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
                self.target_function.branch_tree.print()
                return

        raise NoTargetFunctionException(
            name, 'Cannot find target function definition with given name')
        
    def generate_input(self, target_branch_id):
        fitness_calculator = FitnessCalculator(
            self.target_function, target_branch_id, self.function_defs)

        hc = HillClimbing(fitness_calculator)

        minimised_args, fitness_value = hc.minimise()

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
                branch_type = 'T' if branch[1] is True else 'F'

                branch_id = '{num}{type}'.format(
                    num=branch[0], type=branch_type)
                args = self.generate_input(branch_id)

                inputs[branch_id] = args

            all_inputs[self.target_function.name] = inputs

            if len(next_target_functions) == 0:
                break

            self.set_target_function(next_target_functions.pop())

        return all_inputs

    def _compare_branch_id(self, item):
        id = item[0]

        bnum = int(id[:-1])
        btype = id[-1]

        if btype == 'T':
            return bnum * 2
        elif id[-1] == 'F':
            return bnum * 2 + 1
    
    def generate_all_inputs_and_print(self):
        all_inputs = self.generate_all_inputs()

        for function_name, inputs in all_inputs.items():
            print('[{}]'.format(function_name))

            if len(inputs.items()) == 0:
                print('no branch detected')

            for branch_id, args in sorted(inputs.items(), key=self._compare_branch_id):
                line = '{}:'.format(branch_id)
                if args is None:
                    line += ' -'
                else:
                    for arg in args:
                        line += ' {}'.format(arg)

                print(line)
        
            print('')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python inputgenerator.py <target file location>')
        print(
            '       python inputgenerator.py <target file location> <target function name>')
        exit(1)

    target_file = sys.argv[1]
    target_function = None if len(sys.argv) != 3 else sys.argv[2]

    generator = InputGenerator(target_file, target_function)

    generator.generate_all_inputs_and_print()
