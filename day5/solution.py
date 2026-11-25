from pathlib import Path


def parse_ranges(ranges: str) -> list[tuple[int, int]]:
    return_range = []

    for r in ranges.split():
        start, end = r.split("-")
        return_range.append((int(start), int(end)))

    return return_range


def is_fresh(ranges, f):
    return any(start <= int(f) <= end for start, end in ranges)


def is_inclusive(pair1, pair2):
    return pair1[0] <= pair2[0] <= pair1[1] or pair2[0] <= pair1[1] <= pair2[1]


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not len(ranges):
        return []

    output = []
    pre = ranges[0]
    for cur in ranges:
        if is_inclusive(pre, cur):
            pre = (min(pre[0], cur[0]), max(pre[1], cur[1]))
        else:
            output.append(pre)
            pre = cur
    output.append(pre)
    return output


def count_ids(ranges=list[tuple[int, int]]) -> int:
    ranges.sort()
    output = merge_ranges(ranges)
    count = [len(range(x, y + 1)) for x, y in output]

    return sum(count)


def main(data: str, version=2):
    raw_ranges, inputs = data.split("\n\n")
    ranges = parse_ranges(raw_ranges)
    fresh = [f for f in inputs.split() if is_fresh(ranges, f)]

    if version == 1:
        return len(fresh)
    else:
        return count_ids(ranges)


def run():
    print(main(Path(__file__).with_name("input.txt").read_text()))


if __name__ == "__main__":
    run()
