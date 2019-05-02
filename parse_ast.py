import astor
import ast


def _parse_attribute(attributes, attribute_name):
    for child in attributes:
        if child[1] == attribute_name:
            return child[0]


def parse_id(attributes):
    return _parse_attribute(attributes, 'id')


def parse_body(attributes):
    return _parse_attribute(attributes, 'body')


def parse_orelse(attributes):
    return _parse_attribute(attributes, 'orelse')


def parse_test(attributes):
    return _parse_attribute(attributes, 'test')


def parse_value(attributes):
    return _parse_attribute(attributes, 'value')


def parse_function_def(attributes):
    function_def = {}
    for attribute in attributes:
        function_def[attribute[1]] = attribute[0]

    return function_def


def parse_function_call(attributes):
    function_call = {}

    for attribute in attributes:
        if attribute[1] == 'func':
            function_name = parse_id(astor.iter_node(attribute[0]))
            function_call['func'] = function_name
        elif attribute[1] == 'args':
            function_call['args'] = list(astor.iter_node(attribute[0]))

    return function_call


def find_all_function_def(body):
    functions = []
    for node in body:
        if isinstance(node, ast.FunctionDef):
            function_def = parse_function_def(astor.iter_node(node))
            functions.append(function_def)

    return functions


def find_target_function(body, function_defs):
    nodes = body

    while len(nodes) > 0:
        next_nodes = []
        for node in nodes:
            if isinstance(node, ast.Call):
                function_call = parse_function_call(astor.iter_node(node))

                for function_def in function_defs:
                    if function_def['name'] == function_call['func']:
                        return function_def

                for arg in function_call['args']:
                    next_nodes.append(arg[0])

            elif isinstance(node, ast.Expr) \
                    or isinstance(node, ast.Assign):
                value = parse_value(astor.iter_node(node))
                next_nodes.append(value)

            elif isinstance(node, ast.If) \
                    or isinstance(node, ast.While) \
                    or isinstance(node, ast.For):
                body = parse_body(astor.iter_node(node))
                orelse = parse_orelse(astor.iter_node(node))

                next_nodes.extend(body)
                next_nodes.extend(orelse)

        nodes = next_nodes


def create_predicates_tree(function_def):

    pass


AST = astor.code_to_ast.parse_file('target/calender.py')
body = parse_body(astor.iter_node(AST))

function_defs = find_all_function_def(body)

'''
If targeting function of test generation isn't set,
simply set 'first called' function as a target
'''
target_function = find_target_function(body, function_defs)

predicate_tree = []
