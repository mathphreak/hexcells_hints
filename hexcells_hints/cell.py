class Cell:
    def __init__(self, revealed, blue, label):
        self.revealed = revealed
        self.blue = blue
        self.label = label

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return NotImplemented
        if self.revealed != other.revealed:
            return False
        if self.blue != other.blue:
            return False
        if self.label != other.label:
            return False
        return True

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        return 'Cell{}'.format(repr((self.revealed, self.blue, self.label)))

    def __str__(self):
        return repr(self)
