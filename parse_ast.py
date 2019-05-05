import astor
import ast

from anytree import RenderTree, Walker, PreOrderIter
from walk_predicates import WalkPredicates
from walk_functiondefs import WalkFunctionDefs
from walk_functioncall import TargetFunctionException, WalkFunctionCall


class ASTParser():
    def __init__(self, source):
        self.AST = astor.code_to_ast.parse_file(source)
        self.target_function = None
        self.predicates_tree = None

        self._find_target_function(self.AST)

    def _find_target_function(self, AST):
        walker = WalkFunctionDefs()
        walker.walk(AST)

        function_defs = walker.get_function_definitions()

        '''
        If targeting function of test generation isn't set,
        simply set 'first called' function as a target
        '''
        walker = WalkFunctionCall()
        walker.walk(AST)

        try:
            self.target_function = walker.target_function(function_defs)

        except TargetFunctionException as err:
            print(err)
            exit(1)

    def insert_hooks(self):
        walker = WalkPredicates()
        walker.walk(self.target_function['node'])

        self.predicates_tree = walker.predicates_tree()

    def print_predicates_tree(self):
        for pre, fill, node in RenderTree(self.predicates_tree):
            predicate = 'root'
            if not node.is_root:
                predicate = astor.to_source(node.ast_node.test).rstrip()
                predicate += ': {}\n'.format(node.type)

            print("%s%s" % (pre, predicate))

    def get_all_branches(self):
        branches = []
        for node in PreOrderIter(self.predicates_tree):
            if node.id != None and node.type != None:
                branches.append((node.id, node.type))
        
        return branches

    def get_nodes_on_path(self, target_branch_id):
        branch_type = True if target_branch_id[-1] == 'T' else False
        branch_num = int(target_branch_id[:-1])

        target_node = None
        for node in PreOrderIter(self.predicates_tree):
            if node.id == branch_num and node.type == branch_type:
                target_node = node

        w = Walker()
        nodes_on_path = [(node.id, node.type) for node in w.walk(self.predicates_tree, target_node)[2]]

        nodes_on_path.reverse()

        return nodes_on_path


    def get_target_function(self):
        return self.target_function


if __name__ == "__main__":

    AST = astor.code_to_ast.parse_file('target/triangle.py')

    walker = WalkFunctionDefs()
    walker.walk(AST)

    function_defs = walker.get_function_definitions()

    '''
    If targeting function of test generation isn't set,
    simply set 'first called' function as a target
    '''
    walker = WalkFunctionCall()
    walker.walk(AST)

    target_function = None

    try:
        target_function = walker.target_function(function_defs)

    except TargetFunctionException as err:
        print(err)
        exit(1)

    target_function_def = target_function['node']

    walker = WalkPredicates()
    walker.walk(target_function_def)

    predicates_tree = walker.predicates_tree()

    for pre, fill, node in RenderTree(predicates_tree):
        source = 'root'
        if not node.is_root:
            source = astor.to_source(node.ast_node.test)

        print("%s%s" % (pre, source))
