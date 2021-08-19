import numpy as np

from impl import calculate_cylinder_area, \
    calculate_conduction_thermal_resistance, \
    calculate_convection_thermal_resistance, \
    calculate_conduction_thermal_resistance_for_cylinder

# Constantes Globales
g_k_hierro = 80  # W / m ˚C
g_d_interior = 5  # cm
g_d_exterior = 5.5  # cm
g_d_fibra = 5.5 + 3 + 3  # cm
g_t_inf_1 = 320  # ˚C
g_ancho_fibra = 3  # cm
g_k_fibra = 0.05  # W / m ˚C
g_t_inf_2 = 5  # ˚C
g_h_interior = 60  # W / m ˚C
g_h_exterior = 18  # W / m ˚C
g_largo = 1  # m


def main():
  # Calcular areas
  area_vapor = calculate_cylinder_area(g_d_interior / 100, g_largo)  # m2
  area_fibra = calculate_cylinder_area(g_d_fibra / 100, g_largo)  # m2

  # Calcula resistencias
  resistencia_vapor = calculate_convection_thermal_resistance(g_h_interior, area_vapor)

  resistencia_exterior = calculate_convection_thermal_resistance(
      g_h_exterior, area_fibra)

  resistencia_hierro = calculate_conduction_thermal_resistance_for_cylinder(
      g_d_interior / 2, g_d_exterior / 2, g_largo, g_k_hierro)

  resistencia_fibra = calculate_conduction_thermal_resistance_for_cylinder(
      g_d_exterior / 2, g_d_fibra / 2, g_largo, g_k_fibra)

  resistencia_total = resistencia_vapor + resistencia_exterior + \
      resistencia_hierro + resistencia_fibra

  print(f"Resistencia: {resistencia_total}")

  Q = (g_t_inf_1 - g_t_inf_2) / resistencia_total

  print(f"Calor: {Q}")

  t_pared = -Q * resistencia_hierro + g_t_inf_1

  print(f"T pared: {t_pared}")

  t_fibra = -Q * resistencia_fibra + t_pared

  print(f"T aislamiento: {t_fibra}")


if __name__ == "__main__":
  main()
