import astor
from anytree import AnyNode


class WalkFunctionDefs(astor.TreeWalk):
    def __init__(self):
        astor.TreeWalk.__init__(self)

        self.function_definitions = []

    def pre_FunctionDef(self):
        arguments_count = len(self.cur_node.args.args)
        function_def = {'name': self.cur_node.name,
                        'node': self.cur_node,
                        'args_count': arguments_count}

        self.function_definitions.append(function_def)

    def get_function_definitions(self):
        return self.function_definitions


if __name__ == "__main__":
    AST = astor.code_to_ast.parse_file('target/calender.py')

    walker = WalkFunctionDefs()
    walker.walk(AST)
