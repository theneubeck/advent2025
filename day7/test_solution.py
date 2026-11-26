import pytest

from day7.solution import count_splits, main, parse_data, play

EXAMPLE = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""


@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(
            EXAMPLE, [list(row) for row in EXAMPLE.splitlines()], id="example"
        ),
        pytest.param("S", [["S"]], id="single-cell"),
        pytest.param(".S.", [[".", "S", "."]], id="single-row"),
        pytest.param(".\n^\n.", [["."], ["^"], ["."]], id="single-column"),
        pytest.param("..\n^.", [[".", "."], ["^", "."]], id="two-by-two"),
        pytest.param("..\n^.\n", [[".", "."], ["^", "."]], id="trailing-newline"),
        pytest.param("", [], id="empty"),
    ],
)
def test_parse_data(data, expected):
    assert parse_data(data) == expected


def test_parse_data_example_shape():
    grid = parse_data(EXAMPLE)
    assert len(grid) == 16
    assert all(len(row) == 15 for row in grid)


def test_parse_data_example_cells():
    grid = parse_data(EXAMPLE)
    assert grid[0][7] == "S"
    assert grid[2][7] == "^"
    assert grid[1] == ["."] * 15


ALGOS = ["recursive", "top_down", "bottom_up"]


SMALL = parse_data(".S.\n.^.\n...")


@pytest.mark.parametrize(
    "y, x",
    [
        pytest.param(3, 1, id="row-past-bottom"),
        pytest.param(10, 1, id="row-far-past-bottom"),
        pytest.param(1, -1, id="col-left-of-grid"),
        pytest.param(1, 3, id="col-right-of-grid"),
        pytest.param(3, 3, id="both-out-of-bounds"),
    ],
)
def test_split_out_of_bounds_is_zero(y, x):
    assert count_splits(SMALL, y, x) == 0


@pytest.mark.parametrize(
    "grid, y, x",
    [
        pytest.param(parse_data(".S."), 0, 1, id="single-row-dots"),
        pytest.param(parse_data(".S.\n...\n..."), 0, 1, id="all-dots"),
        pytest.param(parse_data(".S.\n...\n..."), 2, 0, id="all-dots-bottom-left"),
        pytest.param(parse_data(".S.\n...\n..."), 1, 1, id="below-start"),
    ],
)
def test_split_no_splitters_is_zero(grid, y, x):
    assert count_splits(grid, y, x) == 0


def test_play_easy():
    grid = parse_data(".S.\n...\n.^.")
    assert play(grid) == 1


def test_split_on_splitter_returns_int():
    grid = parse_data(".S.\n.^.\n...")
    assert isinstance(count_splits(grid, 1, 1), int)


@pytest.mark.parametrize("algo", ALGOS)
@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(".S.", 1, id="last-row-dot"),
        pytest.param(".S.\n...\n...", 1, id="column-of-dots"),
        pytest.param(".S.\n^..\n...\n...", 1, id="splitter-beside-beam"),
        pytest.param(".S.\n.^.", 2, id="splitter-right-below-start"),
        pytest.param(".S.\n...\n.^.\n...", 2, id="splitter-further-down"),
        pytest.param("..S..\n..^..\n.....\n.^...", 3, id="one-side-splits-again"),
        pytest.param("..S..\n..^..\n.....\n.^.^.", 4, id="both-sides-split-again"),
        pytest.param(
            "...S...\n...^...\n.......\n..^.^..\n.......\n...^...", 6, id="paths-merge"
        ),
    ],
)
def test_paths(data, expected, algo):
    assert play(parse_data(data), version=2, algo=algo) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(EXAMPLE, 21, id="example"),
        pytest.param("S", 0, id="only-start"),
        pytest.param(".S.\n...\n...", 0, id="no-splitters"),
        pytest.param(".S.\n.^.", 1, id="splitter-right-below-start"),
        pytest.param(".S.\n...\n...\n.^.", 1, id="splitter-further-down"),
        pytest.param(".S.\n...\n^..", 0, id="splitter-not-in-beam"),
        pytest.param("..S..\n..^..\n.....\n.^...", 2, id="two-splitters-in-a-chain"),
    ],
)
def test_main_v1(data, expected):
    assert main(data, version=1) == expected


@pytest.mark.parametrize("algo", ALGOS)
@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(EXAMPLE, 40, id="example"),
        pytest.param("S", 1, id="only-start"),
        pytest.param(".S.\n...\n...", 1, id="no-splitters"),
        pytest.param(".S.\n...\n^..", 1, id="splitter-not-in-beam"),
        pytest.param(".S.\n.^.", 2, id="splitter-right-below-start"),
        pytest.param(".S.\n...\n...\n.^.", 2, id="splitter-further-down"),
        pytest.param("..S..\n..^..\n.....\n.^...", 3, id="one-side-splits-again"),
        pytest.param("..S..\n..^..\n.....\n.^.^.", 4, id="both-sides-split-again"),
        pytest.param(
            "...S...\n...^...\n.......\n..^.^..\n.......\n...^...", 6, id="paths-merge"
        ),
    ],
)
def test_main_v2(data, expected, algo):
    assert main(data, version=2, algo=algo) == expected


def test_unknown_algo_raises():
    with pytest.raises(ValueError):
        main(".S.", version=2, algo="nope")
