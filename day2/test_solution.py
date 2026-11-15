import pytest

from day2.solution import find_invalids, main

EXAMPLE = "".join("""11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124""".split())


# def test_example():
#     assert main(EXAMPLE) is None

@pytest.mark.parametrize(
    "id_range, expected",
    [
        ("11-22", [11, 22]),
        ("95-115", [99, 111]),
        ("998-1012", [999, 1010]),
        ("1188511880-1188511890", [1188511885]),
        ("222220-222224", [222222]),
        ("1698522-1698528", []),
        ("446443-446449", [446446]),
        ("38593856-38593862", [38593859]),
        ("565653-565659", [565656]),
        ("824824821-824824827", [824824824]),
        ("2121212118-2121212124", [2121212121]),
    ],
)
def test_find_invalids(id_range, expected):
    assert find_invalids(id_range) == expected

@pytest.mark.parametrize(
    "data, expected",
    [
        pytest.param(EXAMPLE, 4174379265, id="example"),
        pytest.param("1-9", 0, id="single-digits"),
        pytest.param("11-11", 11, id="single-id-range"),
        pytest.param("10-10", 0, id="single-id-valid"),
        pytest.param("100-999", 4995, id="three-digit-repeats"),
        pytest.param("9-11", 11, id="crosses-digit-length"),
        pytest.param("1-100", 495, id="all-two-digit-doubles"),
        pytest.param("1000-1100", 1010, id="four-digits"),
        pytest.param("123123-123123", 123123, id="six-digits"),
        pytest.param("11-22,33-33", 66, id="multiple-ranges"),
        pytest.param("11-22\n", 33, id="trailing-newline"),
    ],
)
def test_main(data, expected):
    assert main(data) == expected

