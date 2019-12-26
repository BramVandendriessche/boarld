from boarld.gridworld.env.board.Grid import Grid
from boarld.gridworld.env.board.GridCell import Goal, Trap, Obstacle, Start


class Grid1:
    _board_rows = 4
    _board_columns = 4
    _win_state = {Goal(3, 0)}
    _lose_states = set()
    _start = Start(0, 3)
    _blocked_cells = set()
    GRID = Grid(_board_rows, _board_columns, _start, _win_state, _lose_states, _blocked_cells, name='Grid1')


class Grid2:
    _board_rows = 4
    _board_columns = 4
    _win_state = {Goal(3, 0)}
    _lose_states = set()
    _start = Start(1, 2)
    _blocked_cells = {Obstacle(1, 1), Obstacle(2, 1), Obstacle(2, 2), Obstacle(1, 3)}
    GRID = Grid(_board_rows, _board_columns, _start, _win_state, _lose_states, _blocked_cells, name='Grid2')


class Grid3:
    _board_rows = 4
    _board_columns = 4
    _win_state = {Goal(3, 0)}
    _lose_states = {Trap(3, 1)}
    _start = Start(1, 2)
    _blocked_cells = {Obstacle(1, 1), Obstacle(2, 1)}
    GRID = Grid(_board_rows, _board_columns, _start, _win_state, _lose_states, _blocked_cells, name='Grid3')


class Grid4:
    _board_rows = 4
    _board_columns = 4
    _win_state = {Goal(3, 0)}
    _lose_states = set()
    _start = Start(3, 2)
    _blocked_cells = {Obstacle(1, 1), Obstacle(2, 1), Obstacle(3, 1), Obstacle(0, 3), Obstacle(1, 3), Obstacle(2, 3), Obstacle(3, 3)}
    GRID = Grid(_board_rows, _board_columns, _start, _win_state, _lose_states, _blocked_cells, name='Grid4')


class Grid5:
    _board_rows = 4
    _board_columns = 4
    _win_state = {Goal(3, 0)}
    _lose_states = {Trap(1, 1), Trap(1, 3)}
    _start = Start(3, 2)
    _blocked_cells = {Obstacle(2, 1), Obstacle(3, 1), Obstacle(0, 3), Obstacle(2, 3), Obstacle(3, 3)}
    GRID = Grid(_board_rows, _board_columns, _start, _win_state, _lose_states, _blocked_cells, name='Grid5')


class Grid6:
    _board_rows = 5
    _board_columns = 5
    _win_state = {Goal(2, 0)}
    _lose_states = {Trap(1, 1)}
    _start = Start(1, 4)
    _blocked_cells = {Obstacle(0, 0), Obstacle(4, 1), Obstacle(2, 2), Obstacle(1, 3), Obstacle(3, 3)}
    GRID = Grid(_board_rows, _board_columns, _start, _win_state, _lose_states, _blocked_cells, name='Grid6')


class Grid7:
    _board_rows = 6
    _board_columns = 6
    _win_state = {Goal(5, 0)}
    _lose_states = {Trap(3, 1), Trap(1, 0)}
    _start = Start(0, 5)
    _blocked_cells = {Obstacle(1, 1), Obstacle(1, 2), Obstacle(1, 3), Obstacle(2, 3), Obstacle(2, 4), Obstacle(4, 2), Obstacle(5, 2), Obstacle(5, 3),
                      Obstacle(4, 3), Obstacle(5, 4)}
    GRID = Grid(_board_rows, _board_columns, _start, _win_state, _lose_states, _blocked_cells, name='Grid7')
