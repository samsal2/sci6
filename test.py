def repeats(l: list, key) -> list:
  return [i if value == key for i, value in enumerate(l)]


print(repeats([1, 1, 2, 1, 1], 1))
