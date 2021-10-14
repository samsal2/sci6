import numpy as np
from scipy.optimize import fsolve
from impl import calc_chen, calc_re, calc_psi

p = 1000
g = 9.81
u = 0.000953
e = 0.00015 * 0.3048
k_tes = 0
k_codo = 0

# balance 1
b1_PA = 101325
# b1_PB = 0
# b1_zA = 30 * 0.3048
b1_zB = 0
b1_L = 1200 * 0.3048 
b1_D = 0.0508
b1_n_tes = 1
b1_n_codo = 0

# balance 2
# b2_PA = 0
b2_PB = 101325
b2_L = 97.536
b2_D = 0.01905
b2_n_tes = 8
b2_n_codo = 4

# balance 3
# b3_PA = 0
b3_PB = 101325
b3_L = 57.912
b3_D = 0.0254
b3_n_tes = 6
b3_n_codo = 4

def calc_p_tsect(flow, dz):
  a = np.pi * (b1_D / 2) * (b1_D / 2)
  v = flow / a
  ed = e / b1_D
  re = calc_re(p, v, b1_D, u)
  f = calc_chen(ed, re)
  print(flow)
  psi = calc_psi(f, b1_L, b1_D, v, b1_n_tes * k_tes + b1_n_codo * k_codo)

  print(psi)

  def fobj(P):
    return b1_PA / p + g * dz - (P / p + v * v / 2 + psi)
 
  print(fobj(-1))

  return fsolve(fobj, 101325)

def calc_v_a(flow_tsect, z_tsect):
  p_tsect = calc_p_tsect(flow_tsect, 0 - z_tsect)
  a_tsect = np.pi * (b1_D / 2) * (b1_D / 2)
  v_tsect = flow_tsect / a_tsect

  z_a = -11.4
  ed = e / b2_D


  def fobj(v):
    re = calc_re(p, v, b2_D, u)
    f = calc_chen(ed, re)
    psi = calc_psi(f, b2_L, b2_D, v, b2_n_tes * k_tes + b2_n_codo * k_codo)

    lhs = p_tsect / p + g * (z_tsect - z_a) + v_tsect * v_tsect / 2
    rhs = b2_PB / p + v * v / 2 + psi

    return lhs - rhs


  return fsolve(fobj, 0.001)

def calc_v_b(flow_tsect, z_tsect):
  p_tsect = calc_p_tsect(flow_tsect, 0 - z_tsect)
  a_tsect = np.pi * (b1_D / 2) * (b1_D / 2)
  v_tsect = flow_tsect / a_tsect

  z_a = -3.144
  ed = e / b3_D


  def fobj(v):
    re = calc_re(p, v, b3_D, u)
    f = calc_chen(ed, re)
    psi = calc_psi(f, b3_L, b3_D, v, b3_n_tes * k_tes + b3_n_codo * k_codo)

    lhs = p_tsect / p + g * (z_tsect - z_a) + v_tsect * v_tsect / 2
    rhs = b3_PB / p + v * v / 3 + psi

    return lhs - rhs


  return fsolve(fobj, 0.001)
  
    
def calc_flow(v, D):
  return v * np.pi * (D/2) * (D/2)


def calc_flow_a(flow_tsect, z_tsect):
  return calc_flow(calc_v_a(flow_tsect, z_tsect), b2_D)

def calc_flow_b(flow_tsect, z_tsect):
  return calc_flow(calc_v_b(flow_tsect, z_tsect), b3_D)


def main():
  print(calc_flow_a(0.0007, -6))
  print(calc_flow_b(0.0007, -6))

if __name__ == "__main__":
  main()
