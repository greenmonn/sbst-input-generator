from covgen.parser.walk_predicates import WalkPredicates
from covgen.parser.walk_targetfunc import WalkTargetFunction

import copy
import astor


class FunctionDef():
    def __init__(self, node, name, args_count):
        self.node = node
        self.name = name
        self.args_count = args_count
        self.branch_tree = None

    def insert_hooks_on_predicates(self):
        walker = WalkPredicates()
        walker.walk(self.node)

        self.branch_tree = walker.get_branch_tree()

    def to_source(self, AST):
        walker = WalkTargetFunction(self)

        AST = copy.deepcopy(AST)

        walker.walk(AST)

        return compile(AST, '', 'exec')

    def call(self, args):
        source = '{func}('.format(func=self.name)

        for arg in args:
            source += '{arg}, '.format(arg=arg)

        source += 'trace)'

        return source
