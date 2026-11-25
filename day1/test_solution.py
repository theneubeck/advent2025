import pytest

from day1.solution import get_the_number, main

EXAMPLE = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


@pytest.mark.parametrize(
    "current, action, expected",
    [
        (50, "L68", 82),
        (82, "L30", 52),
        (52, "R48", 0),
        (0, "L5", 95),
        (95, "R60", 55),
        (55, "L55", 0),
        (0, "L1", 99),
        (99, "L99", 0),
        (0, "R14", 14),
        (14, "L82", 32),
    ],
)
def test_get_the_number(current, action, expected):
    assert get_the_number(current, action)[0] == expected


@pytest.mark.parametrize(
    "current, action, expected",
    [
        (50, "L68", 1),
        (82, "L30", 0),
        (52, "R48", 1),
        (0, "L5", 0),
        (95, "R60", 1),
        (55, "L55", 1),
        (0, "L1", 0),
        (99, "L99", 1),
        (0, "R14", 0),
        (14, "L82", 1),
        (50, "R1000", 10),
        (0, "R100", 1),
    ],
)
def test_get_the_number_zero_count(current, action, expected):
    assert get_the_number(current, action)[1] == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(EXAMPLE, 3, id="example"),
        pytest.param("", 0, id="empty"),
        pytest.param("R1", 0, id="no-zero"),
        pytest.param("R50", 1, id="right-to-zero"),
        pytest.param("L50", 1, id="left-to-zero"),
        pytest.param("R50\nL50\nR50", 2, id="zero-twice"),
        pytest.param("L50\nR100", 2, id="full-turn-stays-on-zero"),
        pytest.param("L250", 1, id="left-multiple-turns"),
        pytest.param("R1050", 1, id="right-multiple-turns"),
        pytest.param("R50\n\nL10\n", 1, id="blank-lines"),
    ],
)
def test_main(data, expected):
    assert main(data, version=1) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(EXAMPLE, 6, id="example"),
        pytest.param("", 0, id="empty"),
        pytest.param("R1", 0, id="no-zero"),
        pytest.param("R50", 1, id="right-to-zero"),
        pytest.param("L50", 1, id="left-to-zero"),
        pytest.param("R50\nL50\nR50", 2, id="zero-twice"),
        pytest.param("L50\nR100", 2, id="full-turn-stays-on-zero"),
        pytest.param("L250", 3, id="left-multiple-turns"),
        pytest.param("R1050", 11, id="right-multiple-turns"),
        pytest.param("R50\n\nL10\n", 1, id="blank-lines"),
    ],
)
def test_main_v2(data, expected):
    assert main(data, version=2) == expected
