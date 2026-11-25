import pytest

from day7.solution import main, parse_data, split, play, build_paths

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
        pytest.param(EXAMPLE, [list(row) for row in EXAMPLE.splitlines()], id="example"),
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



SMALL = parse_data("...\n.^.\n...")


@pytest.mark.parametrize(
    "x, y",
    [
        pytest.param(3, 1, id="row-past-bottom"),
        pytest.param(10, 1, id="row-far-past-bottom"),
        pytest.param(1, -1, id="col-left-of-grid"),
        pytest.param(1, 3, id="col-right-of-grid"),
        pytest.param(3, 3, id="both-out-of-bounds"),
    ],
)
def test_split_out_of_bounds_is_zero(x, y):
    assert split(SMALL, x, y) == 0


@pytest.mark.parametrize(
    "grid, x, y",
    [
        pytest.param(parse_data("..."), 0, 1, id="single-row-dots"),
        pytest.param(parse_data("...\n...\n..."), 0, 1, id="all-dots"),
        pytest.param(parse_data("...\n...\n..."), 2, 0, id="all-dots-bottom-left"),
        pytest.param(parse_data(".S.\n...\n..."), 1, 1, id="below-start"),
    ],
)
def test_split_no_splitters_is_zero(grid, x, y):
    assert split(grid, x, y) == 0


def test_play_easy():
    grid = parse_data(".S.\n...\n.^.")
    assert play(grid) == 1


def test_split_on_splitter_returns_int():
    grid = parse_data("...\n.^.\n...")
    assert isinstance(split(grid, 1, 1), int)


@pytest.mark.parametrize(
    "x",
    [
        pytest.param(3, id="just-past-bottom"),
        pytest.param(10, id="far-past-bottom"),
    ],
)
def test_paths_past_bottom_is_one_timeline(x):
    assert build_paths(parse_data("...\n...\n..."))(x, 1) == 1


@pytest.mark.parametrize(
    "data, x, y, expected",
    [
        pytest.param("...", 0, 1, 1, id="last-row-dot"),
        pytest.param("...\n...\n...", 0, 1, 1, id="column-of-dots"),
        pytest.param("^..\n...\n...", 1, 1, 1, id="splitter-above-start-ignored"),
        pytest.param(".^.\n...", 0, 1, 2, id="on-splitter"),
        pytest.param("...\n.^.\n...", 0, 1, 2, id="splitter-below"),
        pytest.param("..^..\n.....\n.^...", 0, 2, 3, id="one-side-splits-again"),
        pytest.param("..^..\n.....\n.^.^.", 0, 2, 4, id="both-sides-split-again"),
        pytest.param(
            "...^...\n.......\n..^.^..\n.......\n...^...", 0, 3, 6, id="paths-merge"
        ),
    ],
)
def test_paths(data, x, y, expected):
    assert build_paths(parse_data(data))(x, y) == expected



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
        pytest.param("...S...\n...^...\n.......\n..^.^..\n.......\n...^...", 6, id="paths-merge"),
    ],
)
def test_main_v2(data, expected):
    assert main(data, version=2) == expected
