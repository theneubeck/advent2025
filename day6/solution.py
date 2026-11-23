from math import prod
from pathlib import Path


def solve_version1(columns: list[str]) -> int:
    return sum(
        [apply(numbers, op) for *numbers, op in columns]
    )


def apply(row, operator):
    if operator == "+":
        return sum(map(int, row))
    elif operator == "*":
        return prod(map(int, row))
    else:
        raise ValueError(f"unknown operator: {operator!r}")


def solve_version2(columns: list[str]) -> int:
    return solve_version1(columns)

parse_int = lambda x: None if x == " " else x

def parse_data(data:str):
    rows = data.splitlines()
    operators = rows.pop().split()
    num_rows = len(rows)
    num_cols = max([len(r) for r in rows])
    grid = {
        (r, c): parse_int(ch)
        for r, line in enumerate(rows)
        for c, ch in enumerate(line)
    }
    bas = []
    rr = []
    for c in range(num_cols):
        vals = [grid.get((r, c)) for r in range(num_rows) if grid.get((r, c))]
        if vals:
            rr.append(int("".join(vals)))
        else:
            rr.reverse()
            bas.append((*rr, operators.pop(0), ))
            rr = []
    rr.reverse()
    bas.append((*rr, operators.pop(0), ))
    bas.reverse()
    return bas

def main(data: str, version=2):
    if version == 1:
        rows = [line.split() for line in data.splitlines()]
        columns = list(zip(*rows))
        return solve_version1(columns)
    else:
        return solve_version2(parse_data(data))


def run():
    print(main(Path(__file__).with_name("input.txt").read_text()))


if __name__ == "__main__":
    run()
