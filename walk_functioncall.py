import astor
from anytree import AnyNode


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

        self.function_call.append((name, args, self.cur_node))
        print(name)
        print(args)
        print(astor.to_source(self.cur_node))

    def function_call(self):
        return self.function_call

    def target_function(self, function_defs):
        local_calls = []

        for f in self.function_call:
            for f_def in function_defs:
                if f[0] == f_def[0]: # compare name
                    local_calls.append(f_def[1])

        if len(set(local_calls)) > 1:
            raise TargetFunctionException(set(local_calls),
                'Multiple target function detected. Provide source with only one function call in main.')
        
        elif len(local_calls) == 0:
            raise TargetFunctionException(local_calls,
                'No target function detected. Provide source with only one function call in main.')
        else:
            return local_calls[0]


if __name__ == "__main__":
    AST = astor.code_to_ast.parse_file('target/calender.py')

    walker = WalkFunctionCall()
    walker.walk(AST)
