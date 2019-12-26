from abc import abstractmethod, ABC

from boarld.core.util.observ.Observable import Observable


class Board(Observable, ABC):
    """
    Class representing a board containing cells;
        (x, y) coordinate is the cell in the
            (y-1)th row (top to bottom)
            (x-1)th column (left to right)
    """

    def __init__(self, nb_rows: int, nb_cols: int, name: str = ''):
        """
        Construct a board with "nb_rows" rows, "nb_cols" columns and -optionally- a name.
        :param nb_rows: The number of rows in the board.
        :param nb_cols: The number of columns in the board.
        :param name: The board's name.
        """
        super().__init__()
        self.nb_rows: int = nb_rows
        self.nb_cols: int = nb_cols

        self.cells = self._build_board()
        self.cell_set = set([cell for sublist in self.cells for cell in sublist])
        self.name = name or self._generate_name()

    @abstractmethod
    def _build_board(self):
        """
        Construct the board.
        :return: The resulting array of cells.
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Reset the board.
        :return: None
        """
        pass

    def _generate_name(self) -> str:
        """
        Generate the board's name based on its dimensions.
        :return: The generated name.
        """
        return "%s_%sx%s" % (self.__class__.__name__, self.nb_rows, self.nb_cols)

    def get_cell_at_position(self, x, y):
        """
        Get the Cell at the given coordinates in the board. Uses zero-based indexing, starting in the left upper corner.
        :param x: The x-coordinate
        :param y: The y-coordinate
        :return: The cell at the given position.
        """
        return self.cells[y][x]
