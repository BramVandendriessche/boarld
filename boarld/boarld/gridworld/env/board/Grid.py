from typing import Set, Dict, Tuple

from boarld.core.env.board.Board import Board
from boarld.core.env.board.Cell import Cell
from boarld.gridworld.env.board.GridCell import Start, Goal, Trap, Obstacle


def set_of_cells_to_dict(cells: Set[Cell]) -> Dict[Tuple[int, int], Cell]:
    """
    Construct a dictionary mapping a tuple of coordinates to the cell at this position, from a set of cells.
    :param cells: Set of cells from which the dictionary should be constructed
    :return: A dictionary mapping a tuple of coordinates to the cell at this position.
    """
    res = {}
    for cell in cells:
        res[(cell.x, cell.y)] = cell
    return res


# noinspection PyDefaultArgument
class Grid(Board):
    """
    Gridworld board, containing a start, a set of goals, traps and obstacles.
    """

    def __init__(self, nb_rows: int, nb_cols: int, start: Start, goals: Set[Goal], snake_pits: Set[Trap] = set(),
                 obstacles: Set[Obstacle] = set(), name: str = ''):
        """
        Construct a gridworld board with the given dimensions, start position, set of goals, set of obstacles, set of traps,
        and -optionally- a name.
        :param nb_rows: The number of rows
        :param nb_cols: The number of columns
        :param start: The start position
        :param goals: A set containing target states
        :param snake_pits: A set containing traps
        :param obstacles: A set containing obstacles
        :param name: The grid's name
        """
        if not goals:
            raise ValueError("The board should be given at least one Goal, but none were given.")
        self.start: Start = start
        self.goals: dict = set_of_cells_to_dict(goals)
        self.snake_pits: dict = set_of_cells_to_dict(snake_pits)
        self.obstacles: dict = set_of_cells_to_dict(obstacles)
        super().__init__(nb_rows, nb_cols, name)

    def _build_board(self):

        board = []
        for i in range(self.nb_rows):
            board.append([])
            for j in range(self.nb_cols):
                tmp = Cell(j, i)
                key = (tmp.x, tmp.y)
                if key in self.goals:
                    tmp = self.goals[key]
                elif key in self.snake_pits:
                    tmp = self.snake_pits[key]
                elif key in self.obstacles:
                    tmp = self.obstacles[key]
                elif tmp.has_same_position(self.start):
                    tmp = self.start
                board[i].append(tmp)
        return board

    def reset(self):
        pass

