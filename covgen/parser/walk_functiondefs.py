import astor

from covgen.types.function_def import FunctionDef


class WalkFunctionDefs(astor.TreeWalk):
    def __init__(self):
        astor.TreeWalk.__init__(self)

        self.function_definitions = []

    def pre_FunctionDef(self):
        args_count = len(self.cur_node.args.args)
        function_def = FunctionDef(
            node=self.cur_node, name=self.cur_node.name, args_count=args_count)

        self.function_definitions.append(function_def)

    def get_function_definitions(self):
        return self.function_definitions
