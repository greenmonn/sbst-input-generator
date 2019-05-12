def create_branch_id(branch):
    branch_type = 'T' if branch[1] is True else 'F'

    branch_id = '{num}{type}'.format(
        num=branch[0], type=branch_type)

    return branch_id


def parse_branch_type(id):
    branch_type = True if id[-1] == 'T' else False
    return branch_type


def parse_branch_num(id):
    branch_num = int(id[:-1])
    return branch_num


def parse_branch(id):
    branch_type = parse_branch_type(id)
    branch_num = parse_branch_num(id)

    return (branch_num, branch_type)


def compare_branch_id(item):
    id = item[0]

    bnum = int(id[:-1])
    btype = id[-1]

    if btype == 'T':
        return bnum * 2
    elif id[-1] == 'F':
        return bnum * 2 + 1
