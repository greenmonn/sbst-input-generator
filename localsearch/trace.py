import covgen.localsearch.distance_functions as df


class Trace():
    def __init__(self):
        self.executed_branches = []
    
    def get_executed_branches(self):
      return self.executed_branches

    def is_true(self, id, exp):
        result = self.equals(id, exp, True)
        distance_to_alternative = 0

        if result:
            distance_to_alternative = df.equals_bool(exp, False)

        else:
            distance_to_alternative = df.equals_bool(exp, True)

        self.executed_branches.append((id, result, distance_to_alternative))

        return result

    def is_false(self, id, exp):
        result = self.equals(id, exp, False)
        distance_to_alternative = 0

        if result:
            distance_to_alternative = df.equals_bool(exp, True)

        else:
            distance_to_alternative = df.equals_bool(exp, False)

        self.executed_branches.append((id, result, distance_to_alternative))

        return result

    def equals(self, id, lhs, rhs):
        result = lhs == rhs

        distance_to_alternative = 0

        if result:
            distance_to_alternative = df.not_equals_num(lhs, rhs)

        else:
            distance_to_alternative = df.equals_num(lhs, rhs)

        self.executed_branches.append((id, result, distance_to_alternative))

        return result

    def not_equals(self, id, lhs, rhs):
        result = lhs != rhs

        distance_to_alternative = 0

        if result:
            distance_to_alternative = df.equals_num(lhs, rhs)

        else:
            distance_to_alternative = df.not_equals_num(lhs, rhs)

        self.executed_branches.append((id, result, distance_to_alternative))

        return result

    def less_than(self, id, lhs, rhs):
        result = lhs < rhs

        distance_to_alternative = 0

        if result:
            distance_to_alternative = df.greater_than_or_equals(lhs, rhs)

        else:
            distance_to_alternative = df.less_than(lhs, rhs)

        self.executed_branches.append((id, result, distance_to_alternative))
        return result

    def less_than_or_equals(self, id, lhs, rhs):
        result = lhs <= rhs

        distance_to_alternative = 0

        if result:
            distance_to_alternative = df.greater_than(lhs, rhs)

        else:
            distance_to_alternative = df.less_than_or_equals(lhs, rhs)

        self.executed_branches.append((id, result, distance_to_alternative))
        
        return result

    def greater_than(self, id, lhs, rhs):
        result = lhs > rhs

        distance_to_alternative = 0

        if result:
            distance_to_alternative = df.less_than_or_equals(lhs, rhs)

        else:
            distance_to_alternative = df.greater_than(lhs, rhs)

        self.executed_branches.append((id, result, distance_to_alternative))

        return result

    def greater_than_or_equals(self, id, lhs, rhs):
        result = lhs >= rhs

        distance_to_alternative = 0

        if result:
            distance_to_alternative = df.less_than(lhs, rhs)

        else:
            distance_to_alternative = df.greater_than_or_equals(lhs, rhs)

        self.executed_branches.append((id, result, distance_to_alternative))

        return result
