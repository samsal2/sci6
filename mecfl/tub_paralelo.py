import numpy as np
from scipy.optimize import fsolve
from impl import calc_chen, calc_re, calc_psi 

# Constants
e = 4.572e-5
u = 9e-4
p = 1e3
k_conexion = 0.4
n_conexion_1 = 30
n_conexion_2 = 30
g = 9.80665

def calc_psi_1(flow, l, d):
  a = np.pi * (d/2) * (d/2)
  ed  = e / d
  v = flow / a
  f = calc_chen(ed, calc_re(p, v, d, u))
  return calc_psi(f, l, d, v, n_conexion_1 * k_conexion)

def calc_v_2(flow1, l1, d1, l2, d2):
  psi_1 = calc_psi_1(flow1, l1, d1)
  a = np.pi * (d2/2) * (d2/2)
  ed = e / d2

  def calc_psi_2(v2):
    f = calc_chen(ed, calc_re(p, v2, d2, u))
    return calc_psi(f, l2, d2, v2, n_conexion_2 * k_conexion)

  return fsolve(lambda v2: calc_psi_2(v2) - psi_1, 1)

def calc_flow_2(flow1, l1, d1, l2, d2):
  return calc_v_2(flow1, l1, d1, l2, d2) * np.pi * (d2/2) * (d2/2)

def calc_total_flow(flow1, l1, d1, l2, d2):
  return flow1 + calc_flow_2(flow1, l1, d1, l2, d2)

def calc_flow_1(l1, d1, l2, d2, qt):
  return fsolve(lambda f: calc_total_flow(f, l1, d1, l2, d2) - qt, 1)

def calc_pa_with_psi_1(qt, pa, l1, d1, l2, d2, za, zb):
  flow1 = calc_flow_1(l1, d1, l2, d2, qt)
  psi_1 = calc_psi_1(flow1, l1, d1)
  return p * (pa / p + g * (za - zb) - psi_1)
 
def main(): 
  qt = 0.5663
  za = 6.096
  zb = 15.24
  l1 = 609.6
  d1 = 0.3048
  l2 = 457.2
  d2 = 0.4572
  pa = 689800
  print(calc_pa_with_psi_1(qt, pa, l1, d1, l2, d2, za, zb))

if __name__ == "__main__":
  main()


