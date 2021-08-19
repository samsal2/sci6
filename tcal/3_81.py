import numpy as np
from impl import *

from impl import calculate_cylinder_area, \
    calculate_convection_thermal_resistance, \
    calculate_conduction_thermal_resistance_for_cylinder, \
    calculate_radiation_thermal_resistance

g_t_inf_1 = 90  # ˚C
g_t_inf_2 = 10  # ˚C
g_d_interna = 0.04  # m
g_d_externa = 0.046  # m
g_emisividad = 0.7  # ?
g_h_interna = 120
g_h_externa = 15
g_largo = 15
g_k_hierro = 52


def calcular_resistencia_externa(t_hierro):
  # Calculando areas
  area_externa = calculate_cylinder_area(g_d_externa, g_largo)

  resistencia_externa_1 = calculate_convection_thermal_resistance(g_h_externa, area_externa)

  resistencia_externa_2 = calculate_radiation_thermal_resistance(
      g_emisividad, t_hierro + 273.15, g_t_inf_2 + 273.15, area_externa)

  return sum_parallel_resistances([resistencia_externa_1, resistencia_externa_2])


def calcular_perdida_de_calor(t_hierro):
  # Calculando areas
  area_interna = calculate_cylinder_area(g_d_interna, g_largo)
  area_externa = calculate_cylinder_area(g_d_externa, g_largo)

  # Calculdo resistencias
  resistencia_interna = calculate_convection_thermal_resistance(g_h_interna, area_interna)

  resistencia_hierro = calculate_conduction_thermal_resistance_for_cylinder(
      g_d_interna / 2, g_d_externa / 2, g_largo, g_k_hierro)

  resistencia_externa = calcular_resistencia_externa(t_hierro)

  return (g_t_inf_1 - g_t_inf_2) / sum_linear_resistances([resistencia_interna, resistencia_hierro, resistencia_externa])


def main():

  t_hierro = regula_falsi(g_t_inf_1, g_t_inf_2, 
                          lambda t_hierro: calcular_perdida_de_calor(t_hierro) -
                          (t_hierro - g_t_inf_2) / calcular_resistencia_externa(t_hierro))

  print(f"t_2 = {t_hierro}")
  print(f"q = {calcular_perdida_de_calor(t_hierro)}")


if __name__ == "__main__":
  main()
