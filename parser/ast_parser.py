import astor
import ast

from anytree import RenderTree, Walker, PreOrderIter

from covgen.parser.walk_functiondefs import WalkFunctionDefs


class NoTargetFunctionException(Exception):
    """Exception raised when no target function is found with given name.

    Attributes:
        name -- function name given
        message -- explanation of the error
    """

    def __init__(self, name, message):
        self.name = name
        self.message = message


class ASTParser():
    def __init__(self, source):
        self.AST = astor.code_to_ast.parse_file(source)
        self.function_defs = self._load_function_definitions()
        self.target_function = None
        self.branch_tree = None

    def _load_function_definitions(self):
        walker = WalkFunctionDefs()
        walker.walk(self.AST)

        return walker.get_function_definitions()

    def get_target_function_definition(self, name):
        for f in self.function_defs:
            if f.name == name:
                return f

        raise NoTargetFunctionException(
            name, 'Cannot find target function definition with given name')
