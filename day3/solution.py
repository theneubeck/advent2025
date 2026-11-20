from pathlib import Path


def largest_voltage_version_1_slow(input: str):
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


def largest_voltage_version1(bank: str) -> int:
    if len(bank) < 2:
        raise ValueError(f"bank needs at least 2 digits: {bank!r}")

    # first digit: best candidate, excluding the last position
    first = max(bank[:-1])
    i = bank.index(first)

    # second digit: best candidate after i
    second = max(bank[i + 1:])

    return int(first + second)


def largest_voltage_version2(bank: str) -> int:
    if len(bank) < 12:
        raise ValueError(f"bank needs at least 12 digits: {bank!r}")

    if len(bank) == 12:
        return int(bank)


    start = 0
    digits = []
    for k in range(12):
        end = len(bank) - (12 - k) + 1  # exclusive slice end
        d = max(bank[start:end])
        digits.append(d)
        start = bank.index(d, start) + 1

    return int("".join(digits))


def main(data: str, version=1):
    if version == 1:
        return sum(map(largest_voltage_version1, data.split()))
    else:
        return sum(map(largest_voltage_version2, data.split()))


def run():
    print(main(Path(__file__).with_name("input.txt").read_text()))


if __name__ == "__main__":
    run()
