from pathlib import Path

START = 50
CLICKS = 100


def get_the_number(current: int, action: str) -> int:
    direction, number = action[0], int(action[1:])
    zeros = 0
    if direction == "L":
        propose = current - number
        if propose < 0:
            zeros += int(abs(propose / 100) + 1)
    else:
        propose = current + number
        if propose > 99:
            zeros += int(abs(propose / 100))

    if propose == 0:
        zeros += 1

    if current == 0 and zeros > 0 and direction == "L":
        zeros -= 1
    return propose % 100, zeros


def count_the_zeros(arry) -> int:
    return arry.count(0)


def main(str, version=2):
    entries = str.split()
    result = [50]
    total_zeros = 0
    for entry in entries:
        number, zeros = get_the_number(result[-1], entry)
        total_zeros += zeros
        result.append(number)

    if version == 1:
        return result.count(0)
    else:
        return total_zeros


def run():
    print(main(Path(__file__).with_name("input.txt").read_text()))


if __name__ == "__main__":
    run()
