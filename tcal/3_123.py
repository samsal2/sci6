# %%
import numpy as np
from impl import calculate_cylinder_area, calculate_ring_area, fix_r2

# fig 3-44

g_radio_cilindro = 2.5 / 100  # m
g_radio_aro = 3.0 / 100  # m
g_espesor_aro = 1 / 1000  # m
g_espacio_entre_aros = 3 / 1000  # m
g_t_1 = 180  # ˚C
g_t_2 = 25  # ˚C
g_h = 40  # W / m ˚C
g_l = 1  # m
g_k = 186  # W / m ˚C


def main():
  # sin aletas
  area = calculate_cylinder_area(g_radio_cilindro * 2, g_l)
  q_sin_aletas = g_h * area * (g_t_1 - g_t_2)

  # cilindro 3mm
  area = calculate_cylinder_area(g_radio_cilindro * 2, g_espacio_entre_aros)
  q_cilindro_3mm = g_h * area * (g_t_1 - g_t_2)

  radio_2_corregido = fix_r2(g_radio_aro, g_espesor_aro)

  m = np.sqrt(2 * g_h / (g_k * g_espesor_aro))
  print(m)

  c2 = (2 * g_radio_cilindro / m) / (radio_2_corregido * radio_2_corregido - g_radio_cilindro * g_radio_cilindro)
  print(c2)

  # Tabla 3-4

if __name__ == "__main__":
  main()
