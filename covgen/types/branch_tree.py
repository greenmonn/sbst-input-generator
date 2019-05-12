import astor
from anytree import NodeMixin, RenderTree, Walker, PreOrderIter

import covgen.types.branchutil as branchutil


class BranchNode(NodeMixin):
    def __init__(self, num, type=None, ast_node=None, parent=None):
        self.num = num
        self.type = type
        self.ast_node = ast_node
        self.parent = parent


class BranchTree():
    def __init__(self):
        self.root = BranchNode(num=0, type=None, ast_node=None)

    def print(self):
        for pre, fill, node in RenderTree(self.root):
            if node.is_root:
                predicate = 'root'

            else:
                predicate = astor.to_source(node.ast_node.test).rstrip()
                predicate += ': {}\n'.format(node.type)

            print("%s%s" % (pre, predicate))

    def get_all_branches(self):
        branches = []
        for node in PreOrderIter(self.root):
            if node.num != None and node.type != None:
                branches.append((node.num, node.type))

        return branches

    def get_leaf_branches(self):
        branches = []

        for node in PreOrderIter(self.root):
            if node.is_leaf and node.num != None and node.type != None:
                branches.append((node.num, node.type))

        return branches

    def get_nodes_on_path(self, target_branch_id):
        branch_type = branchutil.parse_branch_type(target_branch_id)
        branch_num = branchutil.parse_branch_num(target_branch_id)

        target_node = None
        for node in PreOrderIter(self.root):
            if node.num == branch_num and node.type == branch_type:
                target_node = node

        w = Walker()
        nodes_on_path = [(node.num, node.type)
                         for node in w.walk(self.root, target_node)[2]]

        nodes_on_path.reverse()

        return nodes_on_path
