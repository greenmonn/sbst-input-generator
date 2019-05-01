'''
입력받은 세 정수가 삼각형을 이룰 수 있으면 True, 아니면 False를 반환
'''

import sys

def is_triangle(longest, m, n):
  if longest < (m + n):
    return True

  return False

def triangle(a, b, c):
  longest = 0
  m = 0
  n = 0

  if (a > b):
    if (a > c):
      longest = a
      m, n = b, c
      
    else:
      longest = c
      m, n = a, b

  else:
    if (b > c):
      longest = b
      m, n = a, c
    else:
      longest = c
      m, n = a, b

  return is_triangle(longest, m, n)


if len(sys.argv) - 1 != 3:
  print("give 3 integers for edges of the triangle as arguments.")
  exit(1)

else:
  a, b, c = map(int, sys.argv[1:])

  print(triangle(a, b, c))
