class Cell:
    """
    Class representing a cell in a Board.
    """
    def __init__(self, x, y):
        """
        Construct a cell at a given (x, y) position in the Board.
        (zero-based indexing, starting from the upper left corner)
        :param x: The cell's x-coordinate.
        :param y: The cell's y-coordinate.
        """
        self.x = x
        self.y = y

    def has_same_position(self, other: 'Cell'):
        """
        Calculate if the given cell is on the same position.
        :param other: The cell to which the cell's coordinates should be compared.
        :return: True if this cell has the same coordinates as the other cell, else False.
        """
        return self.x == other.x and self.y == other.y

    def to_string(self):
        """
        Get a textual representation of the cell.
        :return: A textual representation of the cell.
        """
        return str((self.x, self.y))
