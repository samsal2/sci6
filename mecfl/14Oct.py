import numpy as np
from scipy.optimize import fsolve
from impl import calc_chen, calc_re
import matplotlib.pyplot as plt

#Datos 

g = 9.81
p = 999.96 # kg/m3
t = 15 # ˚C
P_A = 0
P_C = 1 * 101325 # atm man
P_B = 2 * 101325 # atm man
vis = 1.129 / 1000 # cP
e = 4.572e-5 
codo_45 = 0.35
codo_90 = 0.75
valvula_globo = 6
t_linea_recta = 0.4
L_B_x = 90 + 30 + 6
L_C_x = 60 + 60 + 4.5
L_A_x = 3 + 1 + 150

ca_problema = [0, 2.2, 4.5, 6.8, 9, 11.5, 13.6, 15.9, 18, 20.5, 22.7]
cb_problema = [55, 54, 53, 51.5, 49, 45, 42, 39, 35, 32, 27.5]
ef_problema = [0, 13, 23.5, 31.6, 37.5, 42.2, 44, 41.5, 39, 37, 31]


# Cedula 40
ced_40_d_2 = 2.067 * 0.0254 # m
ced_40_d_4 = 4.026 * 0.0254 # m 
ced_40_d_3 = 3.068 * 0.0254 # m

z_B = 6 # m
z_C = 4.5 # m
z_x = 0 # m
z_A = 3

# Rama B
def calc_B_phi(Q_B):
  A = np.pi * ced_40_d_3 * ced_40_d_3 / 4
  v = Q_B / A
  ed = e / ced_40_d_3
  re = calc_re(p, v, ced_40_d_3, vis)
  f = calc_chen(ed, re)
  F = 2 * f * L_B_x / ced_40_d_3 * v * v
  F_accesorios = (codo_45 + codo_90 + valvula_globo + t_linea_recta) * v * v / 2
  return  v * v /2 + P_B / p + g * z_B + F_accesorios + F

def calc_C_phi(Q_C):
  A = np.pi * ced_40_d_2 * ced_40_d_2 / 4
  v = Q_C / A
  ed = e / ced_40_d_3
  re = calc_re(p, v, ced_40_d_2, vis)
  f = calc_chen(ed, re)
  F = 2 * f * L_C_x / ced_40_d_2 * v * v
  F_accesorios = (codo_45 + codo_90 + valvula_globo + t_linea_recta) * v * v / 2
  return  v * v /2 + P_C / p + g * z_C + F_accesorios + F

def calc_Q_C(Q_B):
  def f_obj(Q_C):
    phi_rama_B = calc_B_phi(Q_B)
    phi_rama_C = calc_C_phi(Q_C)
    return (phi_rama_B - phi_rama_C)

  return fsolve(f_obj, 2)

@np.vectorize
def calc_Q_A(Q_B):
  Q_C = calc_Q_C(Q_B) 
  return Q_C + Q_B


@np.vectorize
def calc_H(Q_B):
  Q_C = calc_Q_C(Q_B) 
  Q = Q_C + Q_B
  A = np.pi * ced_40_d_4 * ced_40_d_4 / 4
  v = Q / A
  ed = e / ced_40_d_4
  re = calc_re(p, v, ced_40_d_4, vis)
  f = calc_chen(ed, re)
  F = 2 * f * L_A_x / ced_40_d_4 * v * v
  F_accesorios = (codo_90 + valvula_globo) * v * v / 2
  P_U = (calc_C_phi(Q_C) - v * v / 2) * p
  return (v * v / 2+ g * z_A + P_U / p - P_A / p + F + F_accesorios) / g

Q_B_s = np.linspace(1, 20)
Q_B_h = np.linspace(1/3600, 20/3600)
Q = calc_Q_A(Q_B_h)
H = calc_H(Q_B_h)
plt.plot(ca_problema, cb_problema, label="bomba")
plt.plot(ca_problema, ef_problema, label="eficiencia")
plt.plot(Q_B_s, H, label="teorico")
plt.xlabel("Capacidad (m3/h)")
plt.ylabel("Cabezal (m)")
plt.legend()
plt.grid()
plt.show()



