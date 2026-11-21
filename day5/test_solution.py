import pytest

from day5.solution import main, parse_ranges, is_fresh, is_inclusive, merge_ranges

EXAMPLE = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""


EXAMPLE_RANGES = "3-5\n10-14\n16-20\n12-18"


@pytest.mark.parametrize(
    "raw, expected",
    [
        pytest.param(EXAMPLE_RANGES, [(3, 5), (10, 14), (16, 20), (12, 18)], id="example"),
        pytest.param("3-5", [(3, 5)], id="single-range"),
        pytest.param("3-5\n", [(3, 5)], id="trailing-newline"),
        pytest.param("7-7", [(7, 7)], id="single-point-range"),
        pytest.param("98-102", [(98, 102)], id="multi-digit"),
        pytest.param("1-5\n3-8", [(1, 5), (3, 8)], id="overlapping-kept-as-is"),
        pytest.param("1-3\n1-3", [(1, 3), (1, 3)], id="duplicates-kept"),
        pytest.param("10-12\n1-2", [(10, 12), (1, 2)], id="order-kept"),
        pytest.param(
            "1000000000000-1000000000005",
            [(1000000000000, 1000000000005)],
            id="huge-numbers",
        ),
        pytest.param("", [], id="empty"),
    ],
)
def test_parse_ranges(raw, expected):
    assert parse_ranges(raw) == expected


@pytest.mark.parametrize(
    "raw, ingredient, expected",
    [
        # the example, as described in the puzzle
        pytest.param(EXAMPLE_RANGES, 1, False, id="example-1-spoiled"),
        pytest.param(EXAMPLE_RANGES, 5, True, id="example-5-fresh"),
        pytest.param(EXAMPLE_RANGES, 8, False, id="example-8-spoiled"),
        pytest.param(EXAMPLE_RANGES, 11, True, id="example-11-fresh"),
        pytest.param(EXAMPLE_RANGES, 17, True, id="example-17-in-two-ranges"),
        pytest.param(EXAMPLE_RANGES, 32, False, id="example-32-spoiled"),
        # inclusive boundaries
        pytest.param(EXAMPLE_RANGES, 3, True, id="range-start-included"),
        pytest.param(EXAMPLE_RANGES, 2, False, id="just-below-range"),
        pytest.param(EXAMPLE_RANGES, 6, False, id="just-above-range"),
        pytest.param(EXAMPLE_RANGES, 20, True, id="range-end-included"),
        pytest.param(EXAMPLE_RANGES, 21, False, id="just-above-last-range"),
        pytest.param(EXAMPLE_RANGES, 9, False, id="gap-between-ranges"),
        pytest.param(EXAMPLE_RANGES, 15, True, id="covered-only-by-overlap"),
        pytest.param(EXAMPLE_RANGES, 0, False, id="zero"),
        # special ranges
        pytest.param("", 5, False, id="no-ranges"),
        pytest.param("7-7", 7, True, id="single-point-range"),
        pytest.param("7-7", 6, False, id="below-single-point"),
        pytest.param("7-7", 8, False, id="above-single-point"),
        pytest.param("1000000000000-1000000000005", 10**12 + 3, True, id="huge-numbers-inside"),
        pytest.param("1000000000000-1000000000005", 10**12 + 6, False, id="huge-numbers-outside"),
    ],
)
def test_is_fresh(raw, ingredient, expected):
    assert is_fresh(parse_ranges(raw), ingredient) == expected


# Two inclusive ranges overlap if they share at least one ID.
# Pairs come sorted, so pair1 never starts after pair2.
@pytest.mark.parametrize(
    "pair1, pair2, expected",
    [
        pytest.param((1, 5), (3, 8), True, id="partial-overlap"),
        pytest.param((1, 3), (3, 6), True, id="sharing-an-end"),
        pytest.param((1, 10), (3, 4), True, id="second-inside-first"),
        pytest.param((1, 3), (1, 3), True, id="identical"),
        pytest.param((1, 3), (1, 8), True, id="same-start"),
        pytest.param((1, 8), (5, 8), True, id="same-end"),
        pytest.param((7, 7), (7, 7), True, id="same-single-point"),
        pytest.param((1, 10), (7, 7), True, id="range-around-point"),
        pytest.param((1, 3), (4, 6), False, id="adjacent"),
        pytest.param((1, 3), (5, 6), False, id="gap"),
        pytest.param((7, 7), (8, 8), False, id="neighbouring-points"),
        pytest.param(
            (10**12, 2 * 10**12), (2 * 10**12, 3 * 10**12), True, id="huge-sharing-an-end"
        ),
        pytest.param(
            (10**12, 2 * 10**12), (2 * 10**12 + 1, 3 * 10**12), False, id="huge-adjacent"
        ),
    ],
)
def test_is_inclusive(pair1, pair2, expected):
    assert is_inclusive(pair1, pair2) == expected


# Input is sorted, as count_ids sorts before merging.
# Adjacent ranges (1-3, 4-6) share no ID, so they stay separate.
@pytest.mark.parametrize(
    "ranges, expected",
    [
        pytest.param([], [], id="empty"),
        pytest.param([(3, 5)], [(3, 5)], id="single-range"),
        pytest.param(
            [(3, 5), (10, 14), (12, 18), (16, 20)],
            [(3, 5), (10, 20)],
            id="example-sorted",
        ),
        pytest.param([(1, 3), (5, 6)], [(1, 3), (5, 6)], id="gap-not-merged"),
        pytest.param([(1, 3), (4, 6)], [(1, 3), (4, 6)], id="adjacent-not-merged"),
        pytest.param([(1, 5), (3, 8)], [(1, 8)], id="partial-overlap"),
        pytest.param([(1, 3), (3, 6)], [(1, 6)], id="sharing-an-end"),
        pytest.param([(1, 10), (3, 4)], [(1, 10)], id="second-inside-first"),
        pytest.param([(1, 10), (3, 4), (9, 12)], [(1, 12)], id="keeps-widest-end"),
        pytest.param([(1, 3), (1, 3)], [(1, 3)], id="duplicates"),
        pytest.param([(1, 3), (2, 5), (4, 8)], [(1, 8)], id="chain-of-overlaps"),
        pytest.param(
            [(1, 3), (2, 4), (10, 12), (11, 15), (20, 20)],
            [(1, 4), (10, 15), (20, 20)],
            id="several-groups",
        ),
        pytest.param([(7, 7), (7, 7), (8, 8)], [(7, 7), (8, 8)], id="single-points"),
        pytest.param([(0, 2)], [(0, 2)], id="starts-at-zero"),
        pytest.param([(0, 0), (5, 6)], [(0, 0), (5, 6)], id="zero-point-range"),
        pytest.param(
            [(10**12, 2 * 10**12), (2 * 10**12, 3 * 10**12)],
            [(10**12, 3 * 10**12)],
            id="huge-numbers",
        ),
    ],
)
def test_merge_ranges(ranges, expected):
    assert merge_ranges(ranges) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(EXAMPLE, 3, id="example"),
        pytest.param(EXAMPLE.rstrip("\n"), 3, id="no-trailing-newline"),
        pytest.param("3-5\n\n", 0, id="no-ingredients"),
        pytest.param("1-10\n\n1\n5\n10\n", 3, id="all-fresh"),
        pytest.param("1-2\n\n3\n4\n", 0, id="none-fresh"),
        pytest.param("3-5\n\n2\n3\n5\n6\n", 2, id="inclusive-boundaries"),
        pytest.param("1-10\n5-15\n\n7\n", 1, id="overlapping-ranges-count-once"),
        pytest.param("7-7\n\n6\n7\n8\n", 1, id="single-point-range"),
        pytest.param("20-30\n1-5\n\n3\n25\n10\n", 2, id="unsorted-ranges"),
        pytest.param(
            "1000000000000-1000000000005\n\n1000000000003\n999999999999\n",
            1,
            id="huge-numbers",
        ),
    ],
)
def test_main(data, expected):
    assert main(data, version=1) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(EXAMPLE, 14, id="example"),
        pytest.param(EXAMPLE.rstrip("\n"), 14, id="no-trailing-newline"),
        pytest.param("3-5\n\n1\n", 3, id="single-range"),
        pytest.param("7-7\n\n1\n", 1, id="single-point-range"),
        pytest.param("3-5\n\n", 3, id="no-ingredients"),
        pytest.param("3-5\n\n100\n200\n", 3, id="ingredient-ids-ignored"),
        pytest.param("1-5\n3-8\n\n1\n", 8, id="overlapping"),
        pytest.param("1-3\n1-3\n\n1\n", 3, id="duplicate-ranges"),
        pytest.param("1-10\n3-4\n\n1\n", 10, id="range-inside-another"),
        pytest.param("1-3\n4-6\n\n1\n", 6, id="adjacent-ranges"),
        pytest.param("1-3\n3-6\n\n1\n", 6, id="sharing-an-end"),
        pytest.param("1-3\n5-6\n\n1\n", 5, id="gap-between-ranges"),
        pytest.param("10-12\n1-2\n\n1\n", 5, id="unsorted-ranges"),
        pytest.param("1-3\n2-5\n4-8\n\n1\n", 8, id="chain-of-overlaps"),
        pytest.param("1-2\n5-6\n2-5\n\n1\n", 6, id="later-range-bridges-gap"),
        pytest.param("1000000000000-1999999999999\n\n1\n", 10**12, id="huge-range"),
    ],
)
def test_main_v2(data, expected):
    assert main(data, version=2) == expected
