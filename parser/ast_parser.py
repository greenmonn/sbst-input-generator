import astor
import ast

from anytree import RenderTree, Walker, PreOrderIter
from .walk_predicates import WalkPredicates
from .walk_functiondefs import WalkFunctionDefs


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
        self.function_defs = self.load_function_definitions()
        self.target_function = None
        self.branch_tree = None

    def load_function_definitions(self):
        walker = WalkFunctionDefs()
        walker.walk(self.AST)

        return walker.get_function_definitions()

    def set_target_function(self, name):
        for f in self.function_defs:
            if f['name'] == name:
                self.target_function = f
                return

        raise NoTargetFunctionException(
            name, 'Cannot find target function definition with given name')

    def get_target_function_definition(self, name):
        for f in self.function_defs:
            if f['name'] == name:
                return f

        raise NoTargetFunctionException(
            name, 'Cannot find target function definition with given name')

    def insert_hooks(self):
        walker = WalkPredicates()
        walker.walk(self.target_function['node'])

        self.branch_tree = walker.get_branch_tree()

    def print_predicates_tree(self):
        for pre, fill, node in RenderTree(self.branch_tree):
            predicate = 'root'
            if not node.is_root:
                predicate = astor.to_source(node.ast_node.test).rstrip()
                predicate += ': {}\n'.format(node.type)

            print("%s%s" % (pre, predicate))

    def get_all_branches(self):
        branches = []
        for node in PreOrderIter(self.branch_tree):
            if node.id != None and node.type != None:
                branches.append((node.id, node.type))

        return branches

    def get_nodes_on_path(self, target_branch_id):
        branch_type = True if target_branch_id[-1] == 'T' else False
        branch_num = int(target_branch_id[:-1])

        target_node = None
        for node in PreOrderIter(self.branch_tree):
            if node.id == branch_num and node.type == branch_type:
                target_node = node

        w = Walker()
        nodes_on_path = [(node.id, node.type)
                         for node in w.walk(self.branch_tree, target_node)[2]]

        nodes_on_path.reverse()

        return nodes_on_path

    def get_target_function(self):
        return self.target_function

    def get_module_with_target_function(self):
        function_def_nodes = []

        for fdef in self.function_defs:
            if fdef['name'] == self.target_function['name']:
                function_def_nodes.append(self.target_function['node'])
            else:
                function_def_nodes.append(fdef['node'])

        return ast.Module(function_def_nodes)
