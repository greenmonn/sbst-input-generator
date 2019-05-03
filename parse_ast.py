import astor
import ast

from anytree import RenderTree
from walk_predicates import WalkPredicates
from walk_functiondefs import WalkFunctionDefs
from walk_functioncall import TargetFunctionException, WalkFunctionCall

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


walker = WalkPredicates()
walker.walk(target_function)

predicates_tree = walker.predicates_tree()

for pre, fill, node in RenderTree(predicates_tree):
    source = 'root'
    if not node.is_root:
        source = astor.to_source(node.ast_node.test)

    print("%s%s" % (pre, source))
