import copy
from typing import List, Tuple

from boarld.env.action.Action import *
from boarld.env.board.Board import Board
from sliding_puzzle.env.board.PuzzleCell import PuzzleCell
from sliding_puzzle.env.state.State import PuzzleState


class SlidingPuzzle(Board):
    def __init__(self, nb_rows: int, nb_cols: int, sequence: List[int] = None):
        self.init_sequence = sequence
        if sequence is not None and len(sequence) != nb_cols * nb_rows:
            raise ValueError(
                "The given sequence has length %s but expected %s values." % (len(sequence), nb_rows * nb_cols))
        elif sequence is None:
            self.init_sequence = [k for k in range(1, nb_rows * nb_cols)] + [0]
        super().__init__(nb_rows, nb_cols)
        self.value_to_cell_dict = {cell.value: cell for cell in self.cell_set}
        self.zero_cell = self.value_to_cell_dict[0]
        self.init_state = self.puzzle_to_state()
        self.goal_sequence = [[y * self.nb_cols + x + 1 for x in range(self.nb_cols)] for y in range(self.nb_rows)]
        self.goal_sequence[self.nb_rows - 1][self.nb_cols - 1] = 0

    def _build_board(self):
        board = []
        for y in range(self.nb_rows):
            board.append([])
            for x in range(self.nb_cols):
                board[y].append(PuzzleCell(x, y, self.init_sequence[y * self.nb_cols + x]))
        return board

    def get_new_zero_position_after_action(self, current_state: PuzzleState, action: Action.__class__) -> Tuple[
        int, int]:

        new_pos = current_state.zero_position
        if action == Up:
            new_pos = (current_state.zero_position[0], max(0, current_state.zero_position[1] - 1))
        elif action == Down:
            new_pos = (current_state.zero_position[0], min(self.nb_rows - 1, current_state.zero_position[1] + 1))
        elif action == Left:
            new_pos = (max(0, current_state.zero_position[0] - 1), current_state.zero_position[1])
        elif action == Right:
            new_pos = (min(self.nb_cols - 1, current_state.zero_position[0] + 1), current_state.zero_position[1])
        return new_pos

    def get_new_state_after_action(self, current_state: PuzzleState, action: Action.__class__) -> PuzzleState:
        new_pos = self.get_new_zero_position_after_action(current_state, action)
        new_state_data = copy.deepcopy(current_state.data)

        new_state_data[current_state.zero_position[1]][current_state.zero_position[0]] = current_state.data[
            new_pos[1]][new_pos[0]]
        new_state_data[new_pos[1]][new_pos[0]] = 0
        return PuzzleState(new_state_data, new_pos)

    def move(self, action: Action.__class__):
        new_x, new_y = self.get_new_zero_position_after_action(self.puzzle_to_state(), action)

        self.cells[new_y][new_x], self.cells[self.zero_cell.y][self.zero_cell.x] = self.cells[self.zero_cell.y][self.zero_cell.x], self.cells[new_y][new_x]
        self.get_cell_at_position(self.zero_cell.x, self.zero_cell.y).x, self.get_cell_at_position(self.zero_cell.x, self.zero_cell.y).y = self.zero_cell.x, self.zero_cell.y
        self.zero_cell.x, self.zero_cell.y = new_x, new_y
        self.notify_observers_of_change()

        return self.puzzle_to_state()

    def puzzle_to_state(self):
        return PuzzleState([[cell.value for cell in sublist] for sublist in self.cells],
                           (self.zero_cell.x, self.zero_cell.y))

    def set_puzzle_to_solution(self):
        for y in range(self.nb_rows):
            for x in range(self.nb_cols):
                cell = self.value_to_cell_dict[self.goal_sequence[y][x]]
                cell.x, cell.y = x, y
                self.cells[y][x] = cell
        self.notify_observers_of_change()


    def reset(self):
        for y in range(self.nb_rows):
            for x in range(self.nb_cols):
                cell = self.value_to_cell_dict[self.init_sequence[y * self.nb_cols + x]]
                cell.x = x
                cell.y = y
                self.cells[y][x] = cell
        self.notify_observers_of_change()
