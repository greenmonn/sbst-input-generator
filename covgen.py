from parse_ast import ASTParser

from hill_climbing import HillClimbing


class InputGenerator():
    def __init__(self, parser):
        parser.insert_hooks()
        # parser.print_predicates_tree()

        self.parser = parser

    def generate_input(self, target_branch_id):
        nodes_on_path = self.parser.get_nodes_on_path(target_branch_id)

        target_function = self.parser.get_target_function()
        AST = self.parser.get_module_with_target_function()

        hc = HillClimbing(target_function, AST, nodes_on_path)

        minimised_args, fitness_value = hc.minimise()

        # print(minimised_args)
        # print(fitness_value)

        if fitness_value == 0:
            return minimised_args

        else:
            return None

    def generate_all_inputs(self):
        branches = self.parser.get_all_branches()
        # target function의 모든 branch들에 대해서 (1T, 1F, ...)

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


parser = ASTParser('target/calender.py')

generator = InputGenerator(parser)

generator.generate_all_inputs_and_print()
