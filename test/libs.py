import os
from hexcells_hints import Cell, load_image


def grab(file, png=None):
    if png is None:
        png = file.replace('_test.py', '.png')
    return load_image(os.path.join(os.path.dirname(file), png))


def bl():
    return Cell(True, True, '')


def g(n):
    return Cell(True, False, str(n))


def ye():
    return Cell(False, None, None)
