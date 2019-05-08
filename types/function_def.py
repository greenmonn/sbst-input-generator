from covgen.parser.walk_predicates import WalkPredicates

import ast


class FunctionDef():
    def __init__(self, node, name, args_count):
        self.node = node
        self.name = name
        self.args_count = args_count
        self.branch_tree = None
        self.source = None

    def set_compilable_source(self, source):
        self.source = source

    def insert_hooks_on_predicates(self):
        walker = WalkPredicates()
        walker.walk(self.node)

        self.branch_tree = walker.get_branch_tree()

    def to_source(self, function_defs):
        # TODO: handle import, global variables.. etc
        # Just 'substitute' functionDef node of target function, with all other nodes remaining as the same.

        function_def_nodes = []

        for f in function_defs:
            if f.name == self.name:
                function_def_nodes.append(self.node)
            else:
                function_def_nodes.append(f.node)

        return compile(
            ast.Module(function_def_nodes), '', 'exec')

    def call(self, args):
        source = '{func}('.format(func=self.name)

        for arg in args:
            source += '{arg}, '.format(arg=arg)

        source += 'trace)'

        return source
