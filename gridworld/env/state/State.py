from boarld.env.state.State import State
from gridworld.env.board.GridCell import GridCell


class GridState(State):
    def __init__(self, data: GridCell):
        super().__init__(data)