from impl import calculate_cylinder_area
from impl import calculate_convection_thermal_resistance
from impl import calculate_conduction_thermal_resistance_for_cylinder
from impl import regula_falsi
from impl import sum_linear_resistances

g_k_cobre = 223  # BTU / h ft ˚F
g_k_minerales = 0.5  # BTU / h ft ˚F
g_d_interior = 0.4 / 12  # ft
g_d_cobre = 0.6 / 12  # ft
g_d_minerales = g_d_cobre + 0.01 / 12  # ft
g_t_interior = 100  # ˚F
g_t_exterior = 70  # ˚F
g_hv_agua = 1037  # BTU / lbm
g_h_interna = 35  # BTU / h ft2 ˚F
g_h_externa = 1500  # BTU / h ft2 ˚F
g_entrada_agua = 120  # lbm / h


def funcion_objetivo(l):
  # Calculando areas

  area_interior = calculate_cylinder_area(g_d_interior, l)
  area_exterior = calculate_cylinder_area(g_d_minerales, l)

  # Calculando resistencias

  resistencia_interior = calculate_convection_thermal_resistance(g_h_interna, area_interior)

  resistencia_cobre = calculate_conduction_thermal_resistance_for_cylinder(
      g_d_interior / 2, g_d_cobre / 2, l, g_k_cobre)

  resistencia_minerales = calculate_conduction_thermal_resistance_for_cylinder(
      g_d_cobre / 2, g_d_minerales / 2, l, g_k_minerales)

  resistencia_exterior = calculate_convection_thermal_resistance(g_h_externa, area_exterior)

  resistencia_total = sum_linear_resistances(
      [resistencia_interior, resistencia_cobre, resistencia_minerales, resistencia_exterior])

  return (g_t_interior - g_t_exterior) / resistencia_total - g_hv_agua * g_entrada_agua


def main():
  print(f"se ocupan {regula_falsi(902, 2000, funcion_objetivo)} pies de cobre")


if __name__ == "__main__":
  main()
