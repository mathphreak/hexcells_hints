from .libs import grab, bl, g, ye


def test_reg_level():
    orig, actual_level = grab(__file__)
    assert actual_level[0][-1].label == '0'
    assert actual_level[3][7].label == '2'
    assert actual_level[-1][0].label == '0'
    expected_level = [
        [ye(), None, None, None, None, None, None, None, None, None, None, None, None, None, g(0)],
        [None, ye(), None, None, None, None, None, ye(), None, None, None, None, None, ye(), None],
        [ye(), None, ye(), None, None, None, ye(), None, ye(), None, ye(), None, ye(), None, ye()],
        [None, ye(), None, ye(), None, ye(), None, g(2), None, ye(), None, ye(), None, ye(), None],
        [ye(), None, ye(), None, ye(), None, ye(), None, ye(), None, None, None, ye(), None, ye()],
        [None, ye(), None, None, None, None, None, ye(), None, None, None, None, None, ye(), None],
        [g(0), None, None, None, None, None, None, None, None, None, None, None, None, None, ye()]
    ]
    assert actual_level == expected_level


def test_nearly_solved():
    orig, actual_level = grab(__file__, 'Inf_1-2_nearly_solved.png')
    expected_level = [
        [bl(), None, None, None, None, None, None, None, None, None, None, None, None, None, g(0)],
        [None, g(1), None, None, None, None, None, g(2), None, None, None, None, None, g(2), None],
        [g(1), None, g(1), None, None, None, bl(), None, bl(), None, g(0), None, bl(), None, g(1)],
        [None, g(1), None, g(1), None, g(1), None, g(2), None, g(1), None, g(1), None, bl(), None],
        [g(0), None, bl(), None, g(0), None, g(1), None, g(1), None, None, None, g(2), None, g(1)],
        [None, g(1), None, None, None, None, None, g(0), None, None, None, None, None, g(1), None],
        [g(0), None, None, None, None, None, None, None, None, None, None, None, None, None, ye()]
    ]
    assert actual_level == expected_level
