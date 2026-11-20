from pathlib import Path


def largest_voltage(input: str):
    largest = 0
    input_len = len(input)
    for i in range(input_len):
        d = input[i]
        for e in range(i+1, input_len):
            e = input[e]
            num = int(d + e)
            if num > largest:
                largest = num

    return largest




def main(data: str, version=1):
    if version == 1:
        return sum(map(largest_voltage, data.split()))
    else:
        return None


def run():
    print(main(Path(__file__).with_name("input.txt").read_text()))


if __name__ == "__main__":
    run()
