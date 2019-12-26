from boarld.core.env.state.State import State
from boarld.gridworld.env.board.GridCell import GridCell


class GridState(State):
    """
    Class representing an Agent's state in a Grid.
    """
    def __init__(self, data: GridCell):
        """
        Construct a GridState holding the GridCell at which the Agent is currently located.
        :param data: The GridCell at which the Agent is currently located.
        """
        super().__init__(data)
