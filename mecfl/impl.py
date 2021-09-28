import numpy as np

def calc_chen(ed, re):
  b = 0.434294481903252
  a = np.power(ed, 1.1098) / 2.8257 + np.power(7.149 / re, 0.8981)
  f = -4 * (b * np.log((ed / 3.7065) - 5.0452 * (b * np.log(a)) / re))
  return 1 / (f * f)

def calc_re(p, v, d, u):
  return p * v * d / u

def calc_psi(f, l, d, v, sum_k):
  return 2 * f * l / d * v * v + sum_k * v * v / 2

