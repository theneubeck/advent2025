import pytest

from day4.solution import accessible_papers1, accessible_papers2, get_positions, main

EXAMPLE = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


ROWS = EXAMPLE.split()


def row(line: str) -> list[int]:
    return [int(c == "@") for c in line]


@pytest.mark.parametrize(
    "pre, cur, nxt, expected",
    [
        pytest.param([], row(ROWS[0]), row(ROWS[1]), 5, id="row-0"),
        pytest.param(row(ROWS[0]), row(ROWS[1]), row(ROWS[2]), 1, id="row-1"),
        pytest.param(row(ROWS[1]), row(ROWS[2]), row(ROWS[3]), 1, id="row-2"),
        pytest.param(row(ROWS[2]), row(ROWS[3]), row(ROWS[4]), 0, id="row-3"),
        pytest.param(row(ROWS[3]), row(ROWS[4]), row(ROWS[5]), 2, id="row-4"),
        pytest.param(row(ROWS[4]), row(ROWS[5]), row(ROWS[6]), 0, id="row-5"),
        pytest.param(row(ROWS[5]), row(ROWS[6]), row(ROWS[7]), 0, id="row-6"),
        pytest.param(row(ROWS[6]), row(ROWS[7]), row(ROWS[8]), 1, id="row-7"),
        pytest.param(row(ROWS[7]), row(ROWS[8]), row(ROWS[9]), 0, id="row-8"),
        pytest.param(row(ROWS[8]), row(ROWS[9]), [], 3, id="row-9"),
        pytest.param([], [], [], 0, id="empty-row"),
        pytest.param([], [0], [], 0, id="single-empty-cell"),
        pytest.param([], [1], [], 1, id="single-roll"),
        pytest.param([0, 0, 0], [0, 0, 0], [0, 0, 0], 0, id="no-rolls"),
        pytest.param([], [1, 1, 1], [], 3, id="single-row"),
        pytest.param([1], [1], [1], 1, id="column-middle"),
        pytest.param([], [1, 1], [1, 1], 2, id="2x2-full-top"),
        pytest.param([], [1, 1, 1], [1, 1, 1], 2, id="full-top-row-only-corners"),
        pytest.param([1, 1, 1], [1, 1, 1], [], 2, id="full-bottom-row-only-corners"),
        pytest.param([1, 1, 1], [1, 1, 1], [1, 1, 1], 0, id="full-middle-row-none"),
        pytest.param([1] * 5, [1] * 5, [1] * 5, 0, id="5-wide-full-middle-row"),
        pytest.param([], [0, 1, 0], [1, 1, 1], 1, id="plus-top-arm"),
        pytest.param(
            [0, 1, 0], [1, 1, 1], [0, 1, 0], 2, id="plus-centre-has-exactly-4"
        ),
        pytest.param([1, 1, 0], [0, 1, 0], [0, 1, 0], 1, id="exactly-3-neighbours"),
        pytest.param([1, 1, 1], [0, 1, 0], [0, 1, 0], 0, id="exactly-4-neighbours"),
        pytest.param([1, 1, 1], [1, 0, 1], [1, 1, 1], 0, id="empty-cell-not-counted"),
    ],
)
def test_accessible_papers1(pre, cur, nxt, expected):
    assert accessible_papers1(pre, cur, nxt) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        # pytest.param(..., ..., id="..."),
    ],
)
def test_accessible_papers2(data, expected):
    assert accessible_papers2(data) == expected


# Each step of the part 2 example: "x" marks the rolls that get removed.
# Before the step those cells are rolls ("@"), so the input grid is the
# picture with x -> @, and the expected positions are where the x's are.
REMOVAL_STEPS = [
    (
        13,
        """\
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.
""",
    ),
    (
        12,
        """\
.......x..
.@@.x.x.@x
x@@@@...@@
x.@@@@..x.
.@.@@@@.x.
.x@@@@@@.x
.x.@.@.@@@
..@@@.@@@@
.x@@@@@@@.
....@@@...
""",
    ),
    (
        7,
        """\
..........
.x@.....x.
.@@@@...xx
..@@@@....
.x.@@@@...
..@@@@@@..
...@.@.@@x
..@@@.@@@@
..x@@@@@@.
....@@@...
""",
    ),
    (
        5,
        """\
..........
..x.......
.x@@@.....
..@@@@....
...@@@@...
..x@@@@@..
...@.@.@@.
..x@@.@@@x
...@@@@@@.
....@@@...
""",
    ),
    (
        2,
        """\
..........
..........
..x@@.....
..@@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@x.
....@@@...
""",
    ),
    (
        1,
        """\
..........
..........
...@@.....
..x@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...
""",
    ),
    (
        1,
        """\
..........
..........
...x@.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...
""",
    ),
    (
        1,
        """\
..........
..........
....x.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...
""",
    ),
    (
        1,
        """\
..........
..........
..........
...x@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...
""",
    ),
]


def grid_from(text: str) -> dict:
    return {
        (r, c): int(ch == "@")
        for r, line in enumerate(text.split())
        for c, ch in enumerate(line)
    }


def marked_positions(text: str) -> set:
    return {
        (r, c)
        for r, line in enumerate(text.split())
        for c, ch in enumerate(line)
        if ch == "x"
    }


@pytest.mark.parametrize(
    "count, marked",
    [
        pytest.param(count, marked, id=f"step-{i}")
        for i, (count, marked) in enumerate(REMOVAL_STEPS, 1)
    ],
)
def test_get_positions(count, marked):
    grid = grid_from(marked.replace("x", "@"))
    positions = get_positions(grid)
    assert len(positions) == count
    assert set(positions) == marked_positions(marked)


@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(EXAMPLE, 13, id="example"),
        pytest.param(EXAMPLE.rstrip("\n"), 13, id="no-trailing-newline"),
        pytest.param("", 0, id="empty-input"),
        pytest.param(".", 0, id="single-empty-cell"),
        pytest.param("@", 1, id="single-roll"),
        pytest.param("...\n...\n...", 0, id="no-rolls"),
        pytest.param("@@@", 3, id="single-row"),
        pytest.param("@\n@\n@", 3, id="single-column"),
        pytest.param("@@\n@@", 4, id="2x2-full"),
        pytest.param("@@@\n@@@", 4, id="2x3-only-corners"),
        pytest.param("@@@\n@@@\n@@@", 4, id="3x3-only-corners"),
        pytest.param(".@.\n@@@\n.@.", 4, id="plus-centre-has-exactly-4"),
        pytest.param("@@@@@\n" * 5, 4, id="5x5-only-corners"),
    ],
)
def test_main(data, expected):
    assert main(data, version=1) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(EXAMPLE, 43, id="example"),
        pytest.param(EXAMPLE.rstrip("\n"), 43, id="no-trailing-newline"),
        pytest.param("", 0, id="empty-input"),
        pytest.param(".", 0, id="single-empty-cell"),
        pytest.param("@", 1, id="single-roll"),
        pytest.param("...\n...\n...", 0, id="no-rolls"),
        pytest.param("@@@", 3, id="single-row"),
        pytest.param("@\n@\n@", 3, id="single-column"),
        pytest.param("@" * 10, 10, id="long-single-row"),
        pytest.param("@@\n@@", 4, id="2x2-full"),
        pytest.param("@@@\n@@@", 6, id="2x3-full"),
        pytest.param("@@@\n@@@\n@@@", 9, id="3x3-corners-then-arms-then-centre"),
        pytest.param(".@.\n@@@\n.@.", 5, id="plus-arms-then-centre"),
        pytest.param("@@@\n@.@\n@@@", 8, id="ring-corners-then-edges"),
        pytest.param("@@@@@\n" * 5, 4, id="5x5-only-corners-then-stable"),
    ],
)
def test_main_v2(data, expected):
    assert main(data, version=2) == expected
