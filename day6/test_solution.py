import pytest

from day6.solution import main, apply, solve_version1, solve_version2

EXAMPLE = """\
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
"""


@pytest.mark.parametrize(
    "row, operator, expected",
    [
        # the example's four columns
        pytest.param(["123", "45", "6"], "*", 33210, id="example-col-1"),
        pytest.param(["328", "64", "98"], "+", 490, id="example-col-2"),
        pytest.param(["51", "387", "215"], "*", 4243455, id="example-col-3"),
        pytest.param(["64", "23", "314"], "+", 401, id="example-col-4"),
        # edge cases
        pytest.param(["7"], "+", 7, id="single-number-sum"),
        pytest.param(["7"], "*", 7, id="single-number-product"),
        pytest.param(["5", "0", "9"], "*", 0, id="zero-in-product"),
        pytest.param(["0", "0"], "+", 0, id="all-zeros-sum"),
        pytest.param([], "+", 0, id="empty-sum"),
        pytest.param([], "*", 1, id="empty-product"),
        pytest.param([2, 3, 4], "*", 24, id="ints-not-strings"),
        pytest.param(["999999", "999999", "999999"], "*", 999999**3, id="big-product"),
    ],
)
def test_apply(row, operator, expected):
    assert apply(row, operator) == expected


@pytest.mark.parametrize("operator", ["-", "/", "", " ", "x"])
def test_apply_unknown_operator(operator):
    with pytest.raises(ValueError):
        apply(["1", "2"], operator)


@pytest.mark.parametrize(
    "columns, expected",
    [
        pytest.param(
            [
                ("123", "45", "6", "*"),
                ("328", "64", "98", "+"),
                ("51", "387", "215", "*"),
                ("64", "23", "314", "+"),
            ],
            33210 + 490 + 4243455 + 401,
            id="example",
        ),
        pytest.param([("1", "2", "+")], 3, id="single-column"),
        pytest.param([("2", "3", "*"), ("2", "3", "+")], 6 + 5, id="same-numbers-both-ops"),
        pytest.param([("5", "+"), ("5", "*")], 10, id="one-number-per-column"),
        pytest.param([], 0, id="no-columns"),
    ],
)
def test_solve_version1(columns, expected):
    assert solve_version1(columns) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        # pytest.param(..., ..., id="..."),
    ],
)
def test_solve_version2(data, expected):
    assert solve_version2(data) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(EXAMPLE, 4277556, id="example"),
        pytest.param(EXAMPLE.rstrip("\n"), 4277556, id="no-trailing-newline"),
        pytest.param("", 0, id="empty-input"),
        pytest.param("1\n2\n+\n", 3, id="single-column-sum"),
        pytest.param("2\n3\n4\n*\n", 24, id="single-column-product"),
        pytest.param("5 5\n+ *\n", 10, id="one-number-per-column"),
        pytest.param(" 1  2\n10 20\n +  *\n", 51, id="right-aligned-numbers"),
        pytest.param("1  10\n22 3\n+  *\n", 53, id="left-aligned-numbers"),
        pytest.param("   3   4   \n   5   6   \n   *   +   \n", 25, id="extra-surrounding-spaces"),
        pytest.param("0 7\n9 0\n* +\n", 7, id="zeros"),
        pytest.param("1 1 1 1 1\n1 1 1 1 1\n+ * + * +\n", 8, id="many-columns"),
        pytest.param("999999\n999999\n999999\n*\n", 999999**3, id="big-product"),
    ],
)
def test_main(data, expected):
    assert main(data, version=1) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        # pytest.param(EXAMPLE, ..., id="example"),
    ],
)
def test_main_v2(data, expected):
    assert main(data, version=2) == expected
