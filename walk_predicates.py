import astor
from anytree import AnyNode

class WalkPredicates(astor.TreeWalk):
    def __init__(self):
        astor.TreeWalk.__init__(self)

        self.predicates_stack = []
        self.predicates_tree_root = AnyNode(ast_node=None)

    def pre_If(self):
        parent = self.predicates_tree_root
        if len(self.predicates_stack) > 0:
            parent = self.predicates_stack[-1]

        node = AnyNode(ast_node=self.cur_node, parent=parent)
        self.predicates_stack.append(node)

    def post_If(self):
        self.predicates_stack.pop()

    def predicates_tree(self):
        return self.predicates_tree_root
