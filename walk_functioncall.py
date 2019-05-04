import astor
from anytree import AnyNode


def count_functions(functions):
    names = []
    for f in functions:
        if f['name'] not in names:
            names.append(f['name'])

    return len(names)


class TargetFunctionException(Exception):
    """Exception raised for errors in the input.

    Attributes:
        calls -- detected function calls defined in same module
        message -- explanation of the error
    """

    def __init__(self, calls, message):
        self.calls = calls
        self.message = message


class WalkFunctionCall(astor.TreeWalk):
    def __init__(self):
        astor.TreeWalk.__init__(self)

        self.function_call = []
        self.is_in_function_def = False

    def pre_FunctionDef(self):
        self.is_in_function_def = True

    def post_FunctionDef(self):
        self.is_in_function_def = False

    def pre_Call(self):
        if self.is_in_function_def:
            return

        name = self.cur_node.func.id
        args = self.cur_node.args

        self.function_call.append(name)

    def function_call(self):
        return self.function_call

    def target_function(self, function_defs):
        called_functions = []

        for name in self.function_call:
            for f_def in function_defs:
                if name == f_def['name']:
                    called_functions.append(f_def)

        if count_functions(called_functions) > 1:
            raise TargetFunctionException(set(called_functions),
                                          'Multiple target function detected. Provide source with only one function call in main.')

        elif len(called_functions) == 0:
            raise TargetFunctionException(called_functions,
                                          'No target function detected. Provide source with only one function call in main.')
        else:
            return called_functions[0]


if __name__ == "__main__":
    AST = astor.code_to_ast.parse_file('target/calender.py')

    walker = WalkFunctionCall()
    walker.walk(AST)
