
class FunctionDef():
    def __init__(self, node, name, args_count):
        self.node = node
        self.name = name
        self.args_count = args_count
        self.branch_tree = None

    def insert_hooks(self):
        walker = WalkPredicates()
        walker.walk(self.node)

        self.branch_tree = walker.get_branch_tree()
