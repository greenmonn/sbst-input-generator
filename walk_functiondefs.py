import astor
from anytree import AnyNode


class WalkFunctionDefs(astor.TreeWalk):
    def __init__(self):
        astor.TreeWalk.__init__(self)

        self.function_definitions = []

    def pre_FunctionDef(self):
        self.function_definitions.append((self.cur_node.name, self.cur_node))

    def get_function_definitions(self):
        return self.function_definitions


if __name__ == "__main__":
    AST = astor.code_to_ast.parse_file('target/calender.py')

    walker = WalkFunctionDefs()
    walker.walk(AST)
