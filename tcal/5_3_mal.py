import numpy as np

class Solution:
  def __init__(self):
    self.k = 15  # W / m ˚C
    self.h = 80  # W / m2 ˚C
    self.e = 2e6  # W / m3
    self.t_bot = 90  # ˚C
    self.t_inf = 25  # ˚C
    self.q = 5000 # W / m2
    self.delta_x = 1.2e-3 # m
    self.delta_y = 1.2e-3 # m

    # matrix for the solution
    self.__a = np.zeros(shape=(9, 9))
    self.__b = np.zeros(shape=(9))

  def apply_node_1(self):
    # node 1
    top = self.h * self.delta_x / 2
    self.__a[0][0] -= top
    self.__b[0] -= top * self.t_inf
    
    right = self.k * self.delta_y / (2 * self.delta_x)
    self.__a[0][0] -= right
    self.__a[0][1] += right

    bot = self.k * self.delta_x / (2 * self.delta_y)
    self.__a[0][0] -= bot 
    self.__a[0][3] += bot

    self.__b[0] -= self.e * (self.delta_x / 2) * (self.delta_y / 2)

  def apply_node_2(self):
    # node 2
    top = self.h * self.delta_x
    self.__b[1] -= top * self.t_inf
    self.__a[1][1] += top

    right = self.k * self.delta_y / (2 * self.delta_x)
    self.__a[1][1] -= right
    self.__a[1][3] += right

    bot = self.k * self.delta_x / (2 * self.delta_y)
    self.__a[1][1] -= bot
    self.__a[1][4] += bot

    left = self.k * self.delta_y / (2 * self.delta_x)
    self.__a[1][1] -= left
    self.__a[1][0] += left

    self.__b[1] -= self.e * self.delta_x * (self.delta_y / 2)

  def apply_node_3(self):
    # node 3
    top = self.h * (self.delta_x / 2)
    self.__b[2] -= top * self.t_inf
    self.__a[2][2] += top

    right = self.h * (self.delta_y / 2)
    self.__b[2] -= right * self.t_inf
    self.__a[2][2] += right

    bot = self.k * self.delta_x / (2 * self.delta_y)
    self.__a[2][2] -= bot
    self.__a[2][6] += bot

    left = self.k * self.delta_y / (2 * self.delta_x)
    self.__a[2][2] -= left
    self.__a[2][1] += left

    self.__b[2] -= self.e * (self.delta_x / 2) * (self.delta_y / 2)

  def apply_node_4(self):
    top = self.k * self.delta_x / (2 * self.delta_y)
    self.__a[3][3] -= top
    self.__a[3][0] += top

    right = self.k * self.delta_y / (2 * self.delta_x)
    self.__a[3][3] -= right
    self.__a[3][4] += right

    bot = self.k * self.delta_x / (2 * self.delta_y)
    self.__a[3][3] -= bot

    self.__b[3] -= bot * self.t_bot
    self.__b[3] -= self.e * (self.delta_x / 2) * self.delta_y

  def apply_node_5(self):
    top = self.k * self.delta_x / self.delta_y
    self.__a[4][4] -= top
    self.__a[4][0] += top

    right = self.k * self.delta_y / self.delta_x
    self.__a[4][4] -= right
    self.__a[4][5] += right

    bot = self.k * self.delta_x / self.delta_y
    self.__a[4][4] -= bot

    self.__b[4] -= bot * self.t_bot
    self.__b[4] -= self.e * self.delta_x * self.delta_y

  def apply_node_6(self):
    top_conv = self.h * self.delta_x / 2
    self.__a[5][5] -= top_conv
    self.__b[5] -= top_conv * self.t_inf

    top_cond = self.k * self.delta_x / (2 * self.delta_y)
    self.__a[5][5] -= top_cond
    self.__a[5][2] += top_cond

    right_conv = self.h * self.delta_y / 2
    self.__a[5][5] -= right_conv
    self.__b[5] -= right_conv * self.t_inf

    right_cond = self.k * self.delta_y / (2 * self.delta_x)
    self.__a[5][5] -= right_cond
    self.__a[5][6] += right_cond

    bot = self.k * self.delta_x / self.delta_y
    self.__a[5][5] -= bot
    self.__b[5] -= bot * self.t_bot

    self.__b[5] -= 3 * self.e * self.delta_x * self.delta_y / 4

  def apply_node_7(self):
    top = self.h * self.delta_x
    self.__a[6][6] -= top
    self.__b[6] -= top * self.t_inf

    right = self.k * self.delta_y / (2 * self.delta_x)
    self.__a[6][6] -= right
    self.__a[6][7] += right

    bot = self.k * self.delta_x / (2 * self.delta_y)
    self.__a[6][6] -= bot
    self.__b[6] -= bot * self.t_bot

    left = self.k * self.delta_y / (2 * self.delta_x)
    self.__a[6][6] -= left
    self.__a[6][5] += left

    self.__b[6] -= self.e * self.delta_x * self.delta_y / 2
    
  def apply_node_8(self):
    top = self.h * self.delta_x
    self.__a[7][7] -= top
    self.__b[7] -= top * self.t_inf

    right = self.k * self.delta_y / (2 * self.delta_x)
    self.__a[7][7] -= right
    self.__a[7][8] += right

    bot = self.k * self.delta_x / (2 * self.delta_y)
    self.__a[7][7] -= bot
    self.__b[7] -= bot * self.t_bot

    left = self.k * self.delta_y / (2 * self.delta_x)
    self.__a[7][7] -= left
    self.__a[7][6] += left

    self.__b[7] -= self.e * self.delta_x * self.delta_y / 2

  def apply_node_9(self):
    top = self.h * self.delta_x
    self.__a[8][8] -= top
    self.__b[8] -= top * self.t_inf

    right = self.q * self.delta_y / 2
    self.__b[8] -= right

    bot = self.k * self.delta_x / (2 * self.delta_y)
    self.__a[8][8] -= bot
    self.__b[8] -= bot * self.t_bot

    left = self.k * self.delta_y / (2 * self.delta_x)
    self.__a[8][8] -= left
    self.__a[8][7] += left

    self.__b[8] -= self.e * (self.delta_x / 2) * (self.delta_y / 2)

  def solve(self):
    self.apply_node_1()
    self.apply_node_2()
    self.apply_node_3()
    self.apply_node_4()
    self.apply_node_5()
    self.apply_node_6()
    self.apply_node_7()
    self.apply_node_8()
    self.apply_node_9()

    print(self.__a)
    print(self.__b)
    return np.linalg.solve(self.__a, self.__b)
    




def main():
  print(Solution().solve())


if __name__ == "__main__":
    main()
