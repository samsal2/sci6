
from impl import calculate_conduction_thermal_resistance_for_sphere, calculate_convection_thermal_resistance, calculate_sphere_area, sum_linear_resistances

g_t_ebullicion_nitrogeno = -196  # ˚C
g_hv_nitrogeno = 198  # kJ / kg
g_p_nitrogeno = 810  # kg / m3
g_d_interno = 3  # m
g_t_interno = g_t_ebullicion_nitrogeno
g_t_externo = 15  # ˚C
g_h_externo = 35  # W / m ˚C


def calcular_resistencia(espesor=None, k=None):
  # Calculando areas
  # area_interna = calculate_sphere_area(g_d_interno)

  d_externo = g_d_interno + espesor if espesor is not None else g_d_interno

  area_externa = calculate_sphere_area(d_externo)

  # Caculando resistencias

  resistencias = [calculate_convection_thermal_resistance(g_h_externo, area_externa)]

  if espesor is not None:
    resistencias.append(calculate_conduction_thermal_resistance_for_sphere(g_d_interno / 2, d_externo / 2, k))

  return sum_linear_resistances(resistencias)


def calcular_rapidez_de_evaporacion(espesor=None, k=None):
  q = ((g_t_externo - g_t_interno) / calcular_resistencia(espesor, k)) / 1000  # kW
  return (q / (g_p_nitrogeno * g_hv_nitrogeno)) / 3600  # kg / h


def main():
  print(f"a) {calcular_rapidez_de_evaporacion()} kg / h")
  print(f"b) {calcular_rapidez_de_evaporacion(5 / 100, 0.035)} kg / h")
  print(f"c) {calcular_rapidez_de_evaporacion(2 / 100, 0.00005)} kg / h")


if __name__ == "__main__":
  main()
