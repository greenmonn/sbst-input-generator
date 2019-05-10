def boolop_test(a):
    result = a % 10
    result += (a // 10) % 10
    result += (a // 100) % 10

    mult_3 = result % 3 == 0
    mult_4 = result % 4 == 0
    mult_5 = result % 5 == 0

    if mult_3:
        return 3

    elif mult_4:
        return 4

    elif not mult_5:
        return 5
