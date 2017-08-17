from .libs import grab
import pytest


@pytest.mark.xfail(True, reason="image parsing can't handle margin totals yet", run=False)
def test_level():
    orig, actual_level = grab(__file__)
    expected_level = [
        []
    ]
    assert actual_level == expected_level
