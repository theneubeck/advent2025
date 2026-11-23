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


def solve_version2(data: str) -> int:
    raise NotImplementedError


def main(data: str, version=1):
    rows = [line.split() for line in data.splitlines()]
    columns = list(zip(*rows))
    if version == 1:
        return solve_version1(columns)
    else:
        return solve_version2(data)


def run():
    print(main(Path(__file__).with_name("input.txt").read_text()))


if __name__ == "__main__":
    run()
