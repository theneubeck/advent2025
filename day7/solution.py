from functools import lru_cache
from pathlib import Path


def parse_data(data: str):
    rows = data.splitlines()
    grid = []
    for x, row in enumerate(rows):
        if len(grid) <= x:
            grid.append([])
        for char in row:
            grid[x].append(char)

    return grid


def play(grid, version=1, algo="recursive"):
    start = grid[0].index("S")

    if version == 1:
        return count_splits(grid, 1, start)
    elif algo == "recursive":
        return count_paths_recursive(grid, start)
    elif algo == "top_down":
        return count_paths_top_down(grid, start)
    elif algo == "bottom_up":
        return count_paths_bottom_up(grid, start)
    raise ValueError(f"unknown algo: {algo}")


def count_paths_top_down(grid, start):
    table = [[0 for _ in row] for row in grid]
    table[0][start] = 1
    for y, row in enumerate(grid):
        if y == 0:
            continue
        for x, item in enumerate(row):
            if item == ".":
                table[y][x] = table[y][x] + table[y - 1][x]
            elif item == "^":
                if x + 1 < len(row):
                    table[y][x + 1] = table[y][x + 1] + table[y - 1][x]
                if x - 1 >= 0:
                    table[y][x - 1] = table[y][x - 1] + table[y - 1][x]

    return sum(table[-1])


def add_cell(table, origin, dest):
    x, y = origin
    to_x, to_y = dest
    if not (len(table) > to_y >= 0):
        return
    if not (len(table) > y >= 0):
        return
    if not (len(table[to_y]) > to_x >= 0):
        return
    if not (len(table[y]) > x >= 0):
        return

    table[to_y][to_x] = table[to_y][to_x] + table[y][x]


def count_paths_bottom_up(grid, start):
    table = [[0 for _ in row] for row in grid]
    for x, _ in enumerate(table[-1]):
        if grid[-1][x] == "^":
            table[-1][x] = 2
        else:
            table[-1][x] = 1
    for y in range(len(grid) - 1, -1, -1):
        row = grid[y]
        for x, item in enumerate(row):
            if item == "." or item == "S":
                add_cell(table, (x, y + 1), (x, y))
            elif item == "^":
                add_cell(table, (x - 1, y + 1), (x, y))
                add_cell(table, (x + 1, y + 1), (x, y))
    return table[0][start]


def count_paths_recursive(grid, start):

    @lru_cache
    def paths(x, y):
        if x >= len(grid):
            return 1

        if y < 0 or y > len(grid[x]) - 1:
            return 0

        elif grid[x][y] == "^":
            return paths(x + 1, y + 1) + paths(x + 1, y - 1)

        return paths(x + 1, y)

    return paths(0, start)


def count_splits(grid, x, y):
    if x >= len(grid):
        return 0
    if y < 0 or y > len(grid[x]) - 1:
        return 0
    if grid[x][y] == "|":
        return 0

    elif grid[x][y] == "^":
        grid[x][y] = "|"  # mark as visited
        return count_splits(grid, x + 1, y + 1) + count_splits(grid, x + 1, y - 1) + 1

    grid[x][y] = "|"  # mark as visited
    return count_splits(grid, x + 1, y)


def main(data: str, version=2, algo="recursive"):
    grid = parse_data(data)
    return play(grid, version, algo)


def run():
    print(main(Path(__file__).with_name("input.txt").read_text()))


if __name__ == "__main__":
    run()
