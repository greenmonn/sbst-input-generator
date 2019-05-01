'''
년, 월, 일을 입력받으면 요일을 출력해주는 프로그램
'''

import sys
import pytest

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
  days = 0
  for y in range(min(year, 2019), max(year, 2019)):
    if is_leap_year(y):
        days += 366
    
    else:
      days += 365
  
  if year < 2019:
    days = -days
  
  for m in range(1, month):
    if m == 2:
      if is_leap_year(year):
        days += 29
      
      else:
        days += 28

    elif m in [1, 3, 5, 7, 8, 10, 12]:
      days += 31

    else:
      days += 30

  days += date - 1

  return day_string[days % 7]

if __name__ == "__main__":
  if len(sys.argv) - 1 != 3:
    print("give 3 integers for year, month, date as arguments.")
  
  else:
    year, month, date = map(int, sys.argv[1:])
    
    print(find_day_string(year, month, date))
