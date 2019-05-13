import astor

class WalkTargetFunction(astor.TreeWalk):
    def __init__(self, target_function):
        astor.TreeWalk.__init__(self)

        self.target = target_function

    def pre_FunctionDef(self):
        if self.cur_node.name == self.target.name:
            self.cur_node.args = self.target.node.args
            self.cur_node.body = self.target.node.body
            self.cur_node.decorator_list = self.target.node.decorator_list

