import numpy as np


def relative_error(past, current):
  return abs((current - past) / current) * 100


def regula_falsi(upper, lower, f, err=5e-5, __past=None):
  f_upper, f_lower = f(upper), f(lower)

  m = (f_upper - f_lower) / (upper - lower)

  current = -(f_upper / m - upper)

  f_current = f(current)

  if (__past is not None and relative_error(__past, current) < err) or (f_current == 0.0):
    return current

  if f_current * f_upper < 0:
    return regula_falsi(current, upper, f, err, current)

  if f_lower * f_current < 0:
    return regula_falsi(lower, current, f, err, current)

  raise RuntimeError(f"regula_falsi failed with: {f}")


def sum_linear_resistances(resistances):
  return sum(resistances)


def sum_parallel_resistances(resistances):
  return 1 / sum([1 / r for r in resistances])  # bad


def calculate_cylinder_area(d, l):
  return np.pi * d * l


def calculate_sphere_area(d):
  return np.pi * d * d


def fix_r2(r2, t):
  return r2 + t / 2


def calculate_ring_area(r1, r2c):
  return 2 * np.pi * (r2c * r2c - r1 * r1)


def calculate_convection_thermal_resistance(h, area):
  return 1 / (h * area)


def calculate_conduction_thermal_resistance(l, k, area):
  return l / (k * area)


def calculate_conduction_thermal_resistance_for_cylinder(r_1, r_2, l, k):
  return np.log(r_2 / r_1) / (2 * np.pi * l * k)


def calculate_conduction_thermal_resistance_for_sphere(r_1, r_2, k):
  return (r_2 - r_1) / (4 * np.pi * k * r_2 * r_1)


def calculate_radiation_thermal_resistance(epsilon, t_1, t_2, area, sigma=5.67e-8):
  return 1 / (epsilon * sigma * (t_2 * t_2 + t_1 * t_1) * (t_2 + t_1) * area)
