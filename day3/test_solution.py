import pytest

from day3.solution import main, largest_voltage

EXAMPLE = """\
987654321111111
811111111111119
234234234234278
818181911112111
"""


@pytest.mark.parametrize(
    "bank, expected",
    [
        ("987654321111111", 98),
        ("811111111111119", 89),
        ("234234234234278", 78),
        ("818181911112111", 92),
    ],
)
def test_largest_voltage(bank, expected):
    assert largest_voltage(bank) == expected


@pytest.mark.parametrize(
    "bank, expected",
    [
        pytest.param("12", 12, id="two-digits-ascending"),
        pytest.param("21", 21, id="two-digits-descending"),
        pytest.param("11", 11, id="two-equal-digits"),
        pytest.param("99", 99, id="two-nines"),
        pytest.param("1111", 11, id="all-same"),
        pytest.param("123", 23, id="ascending"),
        pytest.param("321", 32, id="descending"),
        pytest.param("1239", 39, id="max-digit-last-cannot-be-first"),
        pytest.param("9123", 93, id="max-digit-first"),
        pytest.param("1991", 99, id="repeated-max-in-middle"),
        pytest.param("9119", 99, id="repeated-max-at-ends"),
        pytest.param("19181", 98, id="max-then-second-best-later"),
        pytest.param("81119", 89, id="first-not-max-but-best-tens"),
        pytest.param("5432198", 98, id="best-pair-at-end"),
    ],
)
def test_largest_voltage_edge_cases(bank, expected):
    assert largest_voltage(bank) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(EXAMPLE, 357, id="example"),
        pytest.param("987654321111111\n", 98, id="single-bank"),
        pytest.param("987654321111111", 98, id="no-trailing-newline"),
        pytest.param("12\n21\n", 33, id="two-short-banks"),
        pytest.param("11\n11\n11\n", 33, id="all-ones"),
        pytest.param("99\n99\n", 198, id="all-nines"),
        pytest.param("1239\n9123\n1991\n", 39 + 93 + 99, id="mixed-banks"),
        pytest.param("\n12\n\n34\n\n", 46, id="blank-lines-ignored"),
        pytest.param("", 0, id="empty-input"),
    ],
)
def test_main(data, expected):
    assert main(data, version=1) == expected


# @pytest.mark.parametrize(
#     "data, expected",
#     [
#         pytest.param(EXAMPLE, None, id="example"),
#     ],
# )
# def test_main_v2(data, expected):
#     assert main(data, version=2) == expected
