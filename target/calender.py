'''
년, 월, 일을 입력받으면 요일을 출력해주는 프로그램
'''

import sys
import pytest


def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 != 0:
            return True
        elif year % 400 == 0:
            return True

    return False


def test_find_day_string():
    assert 'Tuesday' == find_day_string(2019, 1, 1)
    assert 'Sunday' == find_day_string(2019, 4, 28)
    assert 'Wednesday' == find_day_string(2018, 10, 17)


def find_day_string(year, month, date):

  # 2019/1/1: Tuesday
    day_string = [
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday',
        'Monday',
    ]

    days = 0
    y = beforeYear = min(year, 2019)
    afterYear = max(year, 2019)

    while (y < afterYear):
        if is_leap_year(y):
            days += 366

        else:
            days += 365

        y += 1

    if year < 2019:
        days = -days

    m = 1
    while (m < month):
        if m == 2:
            if is_leap_year(year):
                days += 29

            else:
                days += 28

        elif m == 1:
            days += 31

        elif m == 3:
            days += 31

        elif m == 5:
            days += 31

        elif m == 7:
            days += 31

        elif m == 8:
            days += 31

        elif m == 10:
            days += 31

        elif m == 12:
            days += 31

        else:
            days += 30

        m += 1

    days += date - 1

    return day_string[days % 7]


if __name__ == "__main__":
    if len(sys.argv) - 1 != 3:
        print("give 3 integers for year, month, date as arguments.")

    else:
        year, month, date = map(int, sys.argv[1:])

        print(find_day_string(year, month, date))
