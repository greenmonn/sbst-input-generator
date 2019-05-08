import pytest
import astor

from covgen.parser import ast_parser

parser = ASTParser('target/triangle.py')


def test_parse_function_def():
    attributes = astor.iter_node(AST)
    body = parse_body(attributes)

    functions = find_all_function_def(body)

    assert 2 == len(functions)


def test_find_target_function():
    attributes = astor.iter_node(AST)
    body = parse_body(attributes)

    function_defs = find_all_function_def(body)
    target_function = find_target_function(body, function_defs)

    assert 'triangle' == parse_name(list(astor.iter_node(target_function)))
