from functools import lru_cache
from pathlib import Path



def parse_data(data:str):
    rows = data.splitlines()
    grid = []
    for x, row in enumerate(rows):
        if len(grid) <= x:
            grid.append([])
        for y, char in enumerate(row):
            grid[x].append(char)

    return grid



def play(grid, version=1):
    start = grid[0].index("S")

    paths = build_paths(grid)
    if version == 1:
        return split(grid, 1, start)
    else:
        return paths(1, start)


def build_paths(grid):

    @lru_cache
    def paths(x, y):
        if x >= len(grid):
            return 1

        if y < 0 or y > len(grid[x]) - 1:
            return 0

        elif grid[x][y] == "^":
            return paths(x+1, y+1) + paths(x+1,y-1)

        return paths(x+1, y)

    return paths




def split(grid, x, y):
    if x >= len(grid):
        return 0
    if y < 0 or y > len(grid[x]) - 1:
        return 0
    if (grid[x][y] == "|"):
        return 0

    elif grid[x][y] == "^":
        grid[x][y] = "|" # mark as visited
        return split(grid, x+1, y+1) + split(grid, x+1,y-1) + 1

    grid[x][y] = "|" # mark as visited
    return split(grid, x+1, y)

def main(data: str, version=2):
    grid = parse_data(data)
    return play(grid, version)


def run():
    print(main(Path(__file__).with_name("input.txt").read_text()))


if __name__ == "__main__":
    run()
