from boarld.env.board.Cell import Cell


class PuzzleCell(Cell):

    def __init__(self, x, y, value):
        super().__init__(x, y)
        self.value = value
