
def _generate_every_element_except(l, i):
  for j, v in enumerate(l):
    if j != i:
      yield v


def _is_row_valid(row, i):
  abs_sum = sum([abs(a) for a in _generate_every_element_except(row, i)])
  return abs(row[i]) > abs_sum


def _is_strictly_diagonally_dominant(m):
  for i, row in enumerate(m):
    if not _is_row_valid(row, i):
      return False

  return True


def _find_row_strictly_dominant_index(row):
  for i in range(len(row)):
    if _is_row_valid(row, i):
      return i

  assert False


def _make_strictly_diagonally_dominant(a, b):
  infos = [(_find_row_strictly_dominant_index(a_row), a_row, b_val) for a_row, b_val in zip(a, b)]
  sorted_infos = sorted(infos, key=lambda info: info[0])
  return [info[1] for info in sorted_infos], [info[2] for info in sorted_infos]


def _relative_error(new, past):
  return abs((new - past) / new) * 100


def _converged(new, past, err):
  errors = [_relative_error(newv, pastv) for newv, pastv in zip(new, past)]

  for error in errors:
    if error > err:
      return False

  return True


def _iterate_gauss_seidel(a, b, solution):
  new_solution = [v for v in solution]

  for i, row in enumerate(a):
    new_solution[i] = b[i]

    for j, v in enumerate(row):
      if j != i:
        new_solution[i] -= v * new_solution[j]

    new_solution[i] /= row[i]

  return new_solution


def solve(a, b, err=5e-10):
  assert len(a) == len(b)

  if not _is_strictly_diagonally_dominant(a):
    a, b = _make_strictly_diagonally_dominant(a, b)

  past, guess = [0 for _ in b], [1 for _ in b]

  while not _converged(guess, past, err):
    past = guess
    guess = _iterate_gauss_seidel(a, b, past)

  return guess


def main():
  a = [[1, 5, 3],
       [12, 3, -5],
       [3, 7, 13]]
  b = [28, 1, 76]

  print(solve(a, b))


if __name__ == "__main__":
  main()
