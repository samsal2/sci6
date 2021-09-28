import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import gauss_seidel

# Constants
h = 80
k = 15
alpha = 3.2e-6
t_0 = 140
t_inf = 25
t_b = 140
l = 0.015
e = 2e7
q = 8000


def calculate_tau(dt):
  return alpha * dt / (l * l)


def calculate_a(dt):
  tau = calculate_tau(dt)

  a = np.zeros((8, 8))
  a[0][0] = -(h * l / k + 2 + 1 / (2 * tau))
  a[0][1] = 1
  a[0][3] = 1

  a[1][0] = 1
  a[1][1] = -(4 + 2 * h * l / k + 1 / tau)
  a[1][2] = 1
  a[1][4] = 2

  a[2][1] = 1
  a[2][2] = -(2 + 2 * h * l / k + 1 / (2 * tau))
  a[2][5] = 1

  a[3][0] = 1
  a[3][3] = -(4 + 1 / tau)
  a[3][4] = 2

  a[4][1] = 1
  a[4][3] = 1
  a[4][4] = -(4 + 1 / tau)
  a[4][5] = 1

  a[5][2] = 1
  a[5][4] = 2
  a[5][5] = -(6 + 2 * h * l / k + 3 / (2 * tau))
  a[5][6] = 1

  a[6][5] = 1
  a[6][6] = -(4 + 2 * h * l / k + 1 / tau)
  a[6][7] = 1

  a[7][6] = 1
  a[7][7] = -(2 + h * l / k + 1 / (2 * tau))

  return a


def calculate_b(dt, ti):
  tau = calculate_tau(dt)

  b = np.zeros(8)
  b[0] = -(q * l / k + h * l * t_inf / k + l * l * e / (2 * k) + ti[0] / (2 * tau))
  b[1] = -(2 * h * l / k * t_inf + l * l * e / k + ti[1] / tau)
  b[2] = -(2 * h * l * t_inf / k + l * l * e / (2 * k) + ti[2] / (2 * tau))
  b[3] = -(t_b + l * l * e / k + ti[3] / tau + 2 * l * q / k)
  b[4] = -(l * l * e / k + t_b + ti[4] / tau)
  b[5] = -(2 * h * l * t_inf / k + 2 * t_b + 3 * l * l * e / (2 * k) + 3 * ti[5] / (2 * tau))
  b[6] = -(2 * h * l * t_inf / k + 2 * t_b + l * l * e / k + ti[6] / tau)
  b[7] = -(h * l * t_inf / k + t_b + l * l * e / (2 * k) + ti[7] / (2 * tau))

  return b


def create_iterator(dt, solvefn):
  a = calculate_a(dt)

  def iterator(ti):
    b = calculate_b(dt, ti)
    return solvefn(a, b)

  return iterator


def iterate(t, n, solvefn=np.linalg.solve):
  ti = np.zeros(8)
  ti.fill(t_0)

  if n == 0:
    return ti

  iterate = create_iterator(t / n, solvefn)

  for _ in range(n):
    ti = iterate(ti)

  return ti


def create_plot_data(ti):
  return np.array([[t_inf, t_inf, t_inf,  t_inf], [ti[0], ti[1], t_inf, t_inf], [ti[3], ti[4], ti[5], ti[6]]])


def animate(dt):
  x = np.arange(4)
  y = np.flip(np.arange(3))
  fig, ax = plt.subplots(figsize=(8, 8))
  ax.set_yticklabels([])
  ax.set_xticklabels([])
  im = plt.imshow(create_plot_data(iterate(0, 0)), vmin=t_inf, vmax=600)
  # cm = ax.pcolormesh(x, y, create_plot_data(iterate(0, 0)), vmin=20, vmax=600, shading="auto")
  props = {"boxstyle": "round", "facecolor": "wheat", "alpha": 0.5}
  time_label = ax.text(0.05, 0.95, f"$t={0}s$", transform=ax.transAxes, fontsize=14,
                       verticalalignment='top', bbox=props)
  color_bar = fig.colorbar(im, location="bottom")

  def fn(i):
    ti = iterate(dt * (i + 1), 150)
    time_label.set_text(f"$t={i * dt}s$")
    im.set_data(create_plot_data(ti))
    # cm.set_array(create_plot_data(ti).flatten())

  ani = animation.FuncAnimation(fig, fn, np.arange(0, 100),
                                interval=20, blit=False)

  # ani.save("anim.gif")

  plt.show()


def main():
  print(iterate(2 * 60, 160, gauss_seidel.solve))
  animate(5)


if __name__ == "__main__":
  main()
