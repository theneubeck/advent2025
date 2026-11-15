from pathlib import Path

def is_repeated(id):
    return any(
        id == id[:size] * (len(id) // size)
        for size in range(1, len(id) // 2 + 1)
        if len(id) % size == 0
    )


def find_invalids(line):
    start, end = line.split("-")
    return [n for n in range(int(start), int(end) + 1) if is_repeated(str(n))]


def main(data: str):
    lines  = data.split(",")
    invalids = []
    for line in lines:
        if invalid := find_invalids(line):
            invalids.extend(invalid)
    return sum(invalids)


def run():
    print(main(Path(__file__).with_name("input.txt").read_text()))


if __name__ == "__main__":
    run()
