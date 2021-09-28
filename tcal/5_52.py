import numpy as np


class Solution:
  def solve(self):
    a = np.zeros(shape=(3, 3))
    b = np.zeros(shape=(3))

    # nota, t_2 = t_3 = t_5; t_4 = t_6
    # idx 0: t_1, idx 1: t_2, idx 2: t_4

    # nodo 1
    # 300 + 2 * t_2 - 4 * t_1 = 0
    b[0] = -300
    a[0][0] = -4
    a[0][1] = 2

    # nodo 2
    # 200 + t_4 + t_1 - 3 * t_2 = 0
    b[1] = -200
    a[1][0] = 1
    a[1][1] = -3
    a[1][2] = 1

    # nodo 4
    # 500 + 2 * t_2 - 4 * t_4 = 0
    b[2] = -500
    a[2][1] = 2
    a[2][2] = -4

    return np.linalg.solve(a, b),


def main():
  print(Solution().solve())


if __name__ == "__main__":
  main()
