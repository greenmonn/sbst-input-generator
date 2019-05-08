from anytree import NodeMixin, RenderTree

class BranchTree(NodeMixin):
  def __init__(self, id, type=None, ast_node=None, parent=None):
    self.id = id
    self.type = type
    self.ast_node = ast_node
    self.parent = parent
