import os
from hexcells_hints import Cell, load_image


def grab(file, png=None):
    if png is None:
        png = file.replace('_test.py', '.png')
    return load_image(os.path.join(os.path.dirname(file), png))


def bl():
    """Create a blue Cell."""
    return Cell(True, True, '')


def g(n):
    """Create a grey Cell with the given label."""
    return Cell(True, False, str(n))


def ye():
    """Create a yellow Cell."""
    return Cell(False, None, None)


def t(n):
    """Create a grey Cell with {n} - all *t*ogether."""
    return Cell(True, False, "{" + str(n) + "}")


def s(n):
    """Create a grey Cell with -n- - all *s*eparate."""
    return Cell(True, False, "-" + str(n) + "-")
