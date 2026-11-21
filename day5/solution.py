from pathlib import Path

def parse_ranges(ranges: str) -> list[tuple[int, int]]:
    return_range = []

    for r in ranges.split():
        start, end = r.split("-")
        return_range.append((int(start), int(end)))

    return return_range

def is_fresh(ranges, f):
    return any(start <= int(f) <= end for start, end in ranges)

def main(data: str, version=1):
    raw_ranges, inputs = data.split("\n\n")
    ranges = parse_ranges(raw_ranges)
    fresh = [f for f in inputs.split() if is_fresh(ranges, f)]

    if version == 1:
        return len(fresh)
    else:
        return 0


def run():
    print(main(Path(__file__).with_name("input.txt").read_text()))


if __name__ == "__main__":
    run()
