import unittest
import pathlib
from dataclasses import dataclass
from typing import Callable


@dataclass
class Galaxy:
    number: int
    x: int
    y: int


def parse_input(input_path: str) -> dict:
    galaxies = []
    galaxy_rows = set()
    galaxy_columns = set()
    filepath_inp = pathlib.Path(__file__).parent.resolve() / input_path
    with open(filepath_inp) as f:
        counter = 1
        for i, line in enumerate(f):
            for j, letter in enumerate(line):
                if letter == '#':
                    galaxies.append(Galaxy(counter, i, j))
                    counter += 1
                    galaxy_rows.add(i)
                    galaxy_columns.add(j)
    result = {
        'galaxies': galaxies,
        'galaxy_rows': galaxy_rows,
        'galaxy_columns': galaxy_columns
    }
    return result


def find_shortest_path(start: Galaxy, finish: Galaxy,
                       galaxy_rows: set, galaxy_columns: set, exp_factor: int) -> int:
    start_x, finish_x = min(start.x, finish.x), max(start.x, finish.x)
    start_y, finish_y = min(start.y, finish.y), max(start.y, finish.y)
    x = finish_x
    y = finish_y
    for i in range(start_x, finish_x):
        if i not in galaxy_rows:
            x += exp_factor
    for j in range(start_y, finish_y):
        if j not in galaxy_columns:
            y += exp_factor
    return x - start_x + y - start_y


def play(input_path: str, exp_factor: int) -> int:
    result = 0
    data = parse_input(input_path)
    galaxies = data['galaxies']
    galaxy_rows = data['galaxy_rows']
    galaxy_columns = data['galaxy_columns']
    for i in range(0, len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            result += find_shortest_path(galaxies[i], galaxies[j], galaxy_rows, galaxy_columns, exp_factor)
    return result


class TestGalaxies(unittest.TestCase):
    def test_find_shortest_path(self):
        result = find_shortest_path(Galaxy(5, 5, 1), Galaxy(9, 9, 4), {1, 2, 3, 4, 5, 6, 7, 8, 9},
                                    {1, 2, 3, 4, 5, 6, 7, 8, 9}, 1)
        self.assertEqual(7, result)

        galaxy_rows = {0, 1, 2, 4, 5, 6, 8, 9}
        galaxy_columns = {0, 1, 3, 4, 6, 7, 9}
        result = find_shortest_path(Galaxy(5, 5, 1), Galaxy(9, 9, 4), galaxy_rows, galaxy_columns, 1)
        self.assertEqual(9, result)

        result = find_shortest_path(Galaxy(9, 9, 4), Galaxy(5, 5, 1), galaxy_rows, galaxy_columns, 1)
        self.assertEqual(9, result)

        result = find_shortest_path(Galaxy(1, 0, 3), Galaxy(7, 8, 7), galaxy_rows, galaxy_columns, 1)
        self.assertEqual(15, result)

        result = find_shortest_path(Galaxy(3, 2, 0), Galaxy(6, 6, 9), galaxy_rows, galaxy_columns, 1)
        self.assertEqual(17, result)

        result = find_shortest_path(Galaxy(8, 9, 0), Galaxy(9, 9, 4), galaxy_rows, galaxy_columns, 1)
        self.assertEqual(5, result)

    def test_play(self):
        result = play('inputs_tests/input_day_11_test.dat', 1)
        self.assertEqual(374, result)


if __name__ == '__main__':
    print(play('inputs/input_day_11.dat', 999999))
