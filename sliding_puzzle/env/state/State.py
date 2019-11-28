from typing import List, Tuple

from boarld.env.state.State import State


class PuzzleState(State):
    def __init__(self, data: List[List[int]], zero_position: Tuple[int, int]):
        super().__init__(data)
        self.zero_position = zero_position

    def to_string(self):
        return str(self.data)

    def __hash__(self):
        return hash(str(self.data))

    def __eq__(self, other):
        return isinstance(other, PuzzleState) and self.data == other.data and self.zero_position == other.zero_position
