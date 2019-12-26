from boarld.core.env.board.Cell import Cell


class PuzzleCell(Cell):
    """
    Cell in a SlidingPuzzle; extension of Cell including the value of the cell.
    """
    def __init__(self, x, y, value):
        super().__init__(x, y)
        self.value = value
