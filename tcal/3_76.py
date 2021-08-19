import numpy as np

from impl import calculate_cylinder_area, \
    calculate_conduction_thermal_resistance, \
    calculate_convection_thermal_resistance, \
    calculate_conduction_thermal_resistance_for_cylinder, sum_linear_resistances

g_largo = 2  # m
g_d_1 = 40 / 100  # m
g_d_2 = 46 / 100  # m
g_d_3 = 52 / 100  # m
g_t_inf_1 = 55  # ˚C
g_t_inf_2 = 27  # ˚C
g_h_interna = 50  # W / m ˚C
g_h_externa = 12  # W / m ˚C
g_k_espuma = 0.03  # W / m ˚C
g_k_fibra = 0.035  # W / m ˚C
g_costo_inicial = 30
g_costo_energia = 0.08 / 1000  # W / h


def calcular_resistencia_sin_fibra():
  # Areas
  area_1 = calculate_cylinder_area(g_d_1, g_largo)
  area_2 = calculate_cylinder_area(g_d_2, g_largo)

  # Resistencias
  resistencia_1 = calculate_convection_thermal_resistance(g_h_interna, area_1)

  resistencia_2 = calculate_conduction_thermal_resistance_for_cylinder(
      g_d_1 / 2, g_d_2 / 2, g_largo, g_k_espuma)

  resistencia_3 = calculate_convection_thermal_resistance(g_h_externa, area_2)

  return sum_linear_resistances([resistencia_1, resistencia_2, resistencia_3])


def calcular_resistencia_con_fibra():
  # Areas
  area_1 = calculate_cylinder_area(g_d_1, g_largo)
  area_3 = calculate_cylinder_area(g_d_3, g_largo)

  # Resistencias
  resistencia_1 = calculate_convection_thermal_resistance(g_h_interna, area_1)

  resistencia_2 = calculate_conduction_thermal_resistance_for_cylinder(
      g_d_1 / 2, g_d_2 / 2, g_largo, g_k_espuma)

  resistencia_3 = calculate_conduction_thermal_resistance_for_cylinder(
      g_d_2 / 2, g_d_3 / 2, g_largo, g_k_fibra)

  resistencia_4 = calculate_convection_thermal_resistance(g_h_externa, area_3)

  return resistencia_1 + resistencia_2 + resistencia_3 + resistencia_4


def main():
  resistencia_sin_fibra = calcular_resistencia_sin_fibra()
  resistencia_con_fibra = calcular_resistencia_con_fibra()

  q_sin_fibra = (g_t_inf_1 - g_t_inf_2) / resistencia_sin_fibra
  q_con_fibra = (g_t_inf_1 - g_t_inf_2) / resistencia_con_fibra

  # 30 + t * costo * q_con_fibra = t * costo * q_sin_fibra
  # 30 + t * costo * (q_con_fibra - q_sin_fibra) = 0

  t = -g_costo_inicial / (g_costo_energia * (q_con_fibra - q_sin_fibra))

  print(f" Tardaria: {t / 8760} años")


if __name__ == "__main__":
  main()
