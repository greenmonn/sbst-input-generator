import astor

from covgen.parser.walk_functiondefs import WalkFunctionDefs


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
