from pathlib import Path

START = 50
CLICKS = 100


def get_the_number(current: int, action: str) -> int:
    direction, number = action[0], int(action[1:])
    if direction == "L":
        propose = current - number
    else:
        propose = current + number
    return propose % 100

def count_the_zeros(arry) -> int:
    return arry.count(0)



def main(str):
    entries = str.split()
    result = [50]
    for entry in entries:
        result.append(get_the_number(result[-1], entry))

    return result.count(0)

def run():
    print(main(Path(__file__).with_name("input.txt").read_text()))


if __name__ == "__main__":
    run()
