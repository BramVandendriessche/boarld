from abc import abstractmethod, ABC

from boarld.util.observ.Observable import Observable


class Board(Observable, ABC):
    """
    Class representing a board containing cells;
        (x, y) coordinate is the cell in the
            (y-1)th row (top-down)
            (x-1)th column (left to right)
    """

    def __init__(self, nb_rows: int, nb_cols: int):
        super().__init__()
        self.nb_rows: int = nb_rows
        self.nb_cols: int = nb_cols

        self.cells = self._build_board()
        self.cell_set = set([cell for sublist in self.cells for cell in sublist])

    @abstractmethod
    def _build_board(self): pass

    @abstractmethod
    def reset(self): pass

    def get_cell_at_position(self, x, y):
        return self.cells[y][x]
