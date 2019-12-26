from typing import List, Tuple

from boarld.core.env.state.State import State


class PuzzleState(State):
    """
    State representing the configuration of a SlidingPuzzle. The state's data consists of a 2D array with the puzzle's
    configuration. A PuzzleState also includes the position of the zero.
    """
    def __init__(self, data: List[List[int]], zero_position: Tuple[int, int]):
        super().__init__(data)
        self.zero_position = zero_position

    def to_string(self):
        return str(self.data)

    def __hash__(self):
        return hash(str(self.data))

    def __eq__(self, other):
        return isinstance(other, PuzzleState) and self.data == other.data and self.zero_position == other.zero_position
