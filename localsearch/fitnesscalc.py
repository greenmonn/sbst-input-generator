from covgen.trace.trace import Trace


def normalize(n):
    alpha = 0.001

    return 1.0 - (1 + alpha)**(-n)

class FitnessCalculator():
    def __init__(self, target_function, target_branch_id, env):
        branch_tree = target_function.branch_tree
        self.nodes_on_path = branch_tree.get_nodes_on_path(target_branch_id)

        self.source = target_function.to_source(env)
        self.target_function = target_function
    
    def get_args_count(self):
        return self.target_function.args_count

    def calculate(self, args):
        trace = Trace()

        exec(self.source, locals())

        eval(self.target_function.call(args))

        executed_branches = trace.get_executed_branches()

        approach_level = 0
        for branch_num, branch_type in self.nodes_on_path:
            for num, result, distance_to_alternative in executed_branches:
                if approach_level == 0:
                    if branch_num == num and branch_type == result:
                        return 0

                if branch_num == num and branch_type != result:
                    return normalize(distance_to_alternative) + approach_level

            approach_level += 1
