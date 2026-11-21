from pathlib import Path

threashold = 4

def val(row: list[int], idx: int) -> int:
    if idx < 0:
        return 0
    if idx >= len(row):
        return 0
    return row[idx]

def accessible_papers1(pre: list[int], cur: list[int], nxt: list[int]) -> int:
    count = 0
    for i in range(len(cur)):
        if val(cur, i) == 1:
            positions = [
                val(pre, i-1), val(pre, i), val(pre, i+1),
                val(cur, i-1), 0,           val(cur, i+1),
                val(nxt, i-1), val(nxt, i), val(nxt, i+1),
            ]
            count += 1 if sum(positions) < threashold else 0
    return count

def accessible_papers2(data: str) -> int:
    raise NotImplementedError


def transform(line:str):
    return [int(c == "@") for c in line]

def main_lists(data: str, version=1):
    rows = [transform(r) for r in data.split()]
    padded = [[]] + rows + [[]]
    number = 0
    for pre, cur, nxt in zip(padded, padded[1:], padded[2:]):
        if version == 1:
            number += accessible_papers1(pre, cur, nxt)
        else:
            number += accessible_papers2(pre, cur, nxt)

    return number


def main_grid(data: str, version=1):
    rows = data.split()
    grid = {
        (r, c): int(ch == "@")
        for r, line in enumerate(rows)
        for c, ch in enumerate(line)
    }
    count = 0

    for (x, y), value in grid.items():
        if value:
            positions = [
                grid.get((x-i, y-j), 0)
                for i in range(-1,2)
                for j in range(-1,2)
            ]
            count += 1 if sum(positions) < threashold + 1 else 0

    return count

def main(*args, **kwars):
    return main_grid(*args, **kwars)

def run():
    print(main(Path(__file__).with_name("input.txt").read_text()))

if __name__ == "__main__":
    run()
