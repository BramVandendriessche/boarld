from typing import Set, Dict, Tuple

from boarld.env.board.Board import Board
from boarld.env.board.Cell import Cell
from gridworld.env.board.GridCell import Start, Goal, SnakePit, Wall


def set_of_cells_to_dict(cells: Set[Cell]) -> Dict[Tuple[int, int], Cell]:
    res = {}
    for cell in cells:
        res[(cell.x, cell.y)] = cell
    return res


# noinspection PyDefaultArgument
class Grid(Board):

    def __init__(self, nb_rows: int, nb_cols: int, start: Start, goals: Set[Goal], snake_pits: Set[SnakePit] = set(),
                 walls: Set[Wall] = set(), name: str = ''):
        if not goals:
            raise ValueError("The board should be given at least one Goal, but none were given.")
        self.start: Start = start
        self.goals: dict = set_of_cells_to_dict(goals)
        self.snake_pits: dict = set_of_cells_to_dict(snake_pits)
        self.walls: dict = set_of_cells_to_dict(walls)
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
                elif key in self.walls:
                    tmp = self.walls[key]
                elif tmp.has_same_position(self.start):
                    tmp = self.start
                board[i].append(tmp)
        return board

    def reset(self):
        pass

