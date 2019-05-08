import sys

from covgen.parser.ast_parser import ASTParser, NoTargetFunctionException

from covgen.types.function_def import FunctionDef
from covgen.types.branch_tree import BranchTree

from covgen.localsearch.hillclimbing import HillClimbing
from covgen.localsearch.fitnesscalc import FitnessCalculator



class InputGenerator():
    def __init__(self, file, function_name=None):
        parser = ASTParser(file)
        self.function_defs = parser.function_defs
        self.target_function = None

        try:
            self.target_function = parser.get_target_function_definition(
                function_name)

        except NoTargetFunctionException as err:
            print('{}: {}'.format(err.message, err.name))
            exit(1)

        self.target_function.insert_hooks_on_predicates()

        self.target_function.branch_tree.print()

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
        branch_tree = self.target_function.branch_tree

        branches = branch_tree.get_all_branches()

        all_inputs = {}

        for branch in branches:
            branch_type = 'T' if branch[1] is True else 'F'

            branch_id = '{num}{type}'.format(num=branch[0], type=branch_type)
            args = self.generate_input(branch_id)

            all_inputs[branch_id] = args

        return all_inputs

    def generate_all_inputs_and_print(self):
        all_inputs = self.generate_all_inputs()

        for branch_id, args in all_inputs.items():
            line = '{}:'.format(branch_id)
            if args is None:
                line += ' -'
            else:
                for arg in args:
                    line += ' {}'.format(arg)

            print(line)


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
