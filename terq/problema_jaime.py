import numpy as np
from scipy.optimize import fsolve

# x_az = ...
# ln gamma_1 en x_az
# ln gamma_2 en x_AZ

# 0 = f1(A12, A21) - ln gamma_1 = g1(A12, A21)
# 0 = f2(A12, A21) - ln gamma_2 = g2(A12, A21)

def create_antoine(a, b, c):
    return lambda t: np.exp(a - b / (c + t))

t_k = 337.65
t_c = 337.65 - 273.15

p_1_sat = create_antoine(14.3145, 2756.22, 228.060)(t_c)
p_2_sat = create_antoine(13.7324, 2548.74, 218.552)(t_c)
p_sys = 101.3

gamma_1_az = p_sys / p_1_sat
gamma_2_az = p_sys / p_2_sat

x_1_az = 0.345


def ln_wilson_gamma_1_(x1, a12, a21):
  x2 = 1 - x1
  a = x1 + a12 * x2
  b = a12 / (x1 + a12 * x2)
  c = a21 / (a21 * x1 + x2)
  return -np.log(a) + x2 * (b - c)

def ln_wilson_gamma_2_(x2, a12, a21):
  x1 = 1 - x2
  a = x2 + a21 * x1
  b = a12 / (x1 + a12 * x2)
  c = a21 / (a21 * x1 + x2)
  return -np.log(a) - x1 * (c - b)

def fobj(a):
  a12, a21 = a
  x_2_az = 1 - x_1_az
  ln_gamma_1 = ln_wilson_gamma_1_(x_1_az, a12, a21)
  ln_gamma_2 = ln_wilson_gamma_2_(x_2_az, a12, a21)
  return [ln_gamma_1 - np.log(gamma_1_az), ln_gamma_2 - np.log(gamma_2_az)]

r = fsolve(fobj, [2, 1])
print(r)
print(fobj(r))




