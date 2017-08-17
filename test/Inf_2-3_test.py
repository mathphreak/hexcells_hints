from .libs import grab, g, ye
import pytest


@pytest.mark.xfail(True, reason="Stuff's broken right now", run=False)
def test_level():
    orig, actual_level = grab(__file__)
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
