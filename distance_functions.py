
K = 1.0


def equals_bool(lhs, rhs):
    if lhs == rhs:
        return 0

    return K


def equals_num(lhs, rhs):
    return abs(lhs - rhs) + K


def not_equals_bool(lhs, rhs):
    if lhs != rhs:
        return 0

    return K


def not_equals_num(lhs, rhs):
    if lhs != rhs:
        return 0

    return K


def less_than(lhs, rhs):
    if lhs < rhs:
        return 0

    return (lhs - rhs) + K


def less_than_or_equals(lhs, rhs):
    if lhs <= rhs:
        return 0

    return (lhs - rhs) + K


def greater_than(lhs, rhs):
    if lhs > rhs:
        return 0

    return (rhs - lhs) + K


def greater_than_or_equals(lhs, rhs):
    if lhs >= rhs:
        return 0

    return (rhs - lhs) + K
