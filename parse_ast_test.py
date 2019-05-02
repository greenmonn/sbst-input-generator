import pytest
import astor
from parse_ast import *

AST = astor.code_to_ast.parse_file('target/triangle.py')


def test_find_all_function_def():
    attributes = astor.iter_node(AST)
    body = parse_body(attributes)

    functions = find_all_function_def(body)

    assert 2 == len(functions)


def test_find_target_function():
    attributes = astor.iter_node(AST)
    body = parse_body(attributes)

    function_defs = find_all_function_def(body)
    target_function = find_target_function(body, function_defs)

    assert 'triangle' == target_function['name']


def test_parse_predicates():
    pass
