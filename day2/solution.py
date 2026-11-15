from pathlib import Path

def find_invalids(line):
    invalids = []
    start, end = line.split("-")
    for n in range(int(start), int(end) + 1):
        id = str(n)
        if len(id) % 2 != 0: continue
        first, second = id[:len(id) // 2], id[len(id) // 2:]
        if first == second or id[0] == "0":
            invalids.append(int(id))
    return invalids


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
