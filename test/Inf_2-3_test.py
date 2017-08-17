from .libs import grab, g, ye, t, s


def test_level():
    orig, actual_level = grab(__file__)
    assert len(actual_level) == 13
    assert len(actual_level[0]) == 7
    expected_level = [
        [None, None, None, g(0), None, None, None],
        [None, None, ye(), None, ye(), None, None],
        [None, ye(), None, ye(), None, ye(), None],
        [ye(), None, ye(), None, ye(), None, ye()],
        [None, t(5), None, None, None, t(3), None],
        [ye(), None, ye(), None, ye(), None, ye()],
        [None, ye(), None, g(2), None, ye(), None],
        [ye(), None, None, None, None, None, ye()],
        [None, g(2), None, ye(), None, s(2), None],
        [ye(), None, ye(), None, ye(), None, ye()],
        [None, ye(), None, ye(), None, ye(), None],
        [None, None, ye(), None, ye(), None, None],
        [None, None, None, g(1), None, None, None]
    ]
    assert actual_level == expected_level
