from boarld.core.env.board.Cell import Cell


class GridCell(Cell):
    """
    Cell in a Grid
    """
    pass


class Start(GridCell):
    """
    GridCell representing a start position.
    """
    pass


class Goal(GridCell):
    """
    GridCell representing a target position.
    """
    pass


class Trap(GridCell):
    """
    GridCell representing a trap.
    """
    pass


class Obstacle(GridCell):
    """
    GridCell representing an obstacle.
    """
    pass
