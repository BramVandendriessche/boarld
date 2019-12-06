# -- BOARD SETUP -- #
from gridworld.env.board.Grid import Grid
from gridworld.env.board.GridCell import Goal, SnakePit, Wall, Start


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
    _blocked_cells = {Wall(1, 1), Wall(2, 1), Wall(2, 2), Wall(1, 3)}
    GRID = Grid(_board_rows, _board_columns, _start, _win_state, _lose_states, _blocked_cells, name='Grid2')


class Grid3:
    _board_rows = 4
    _board_columns = 4
    _win_state = {Goal(3, 0)}
    _lose_states = {SnakePit(3, 1)}
    _start = Start(1, 2)
    _blocked_cells = {Wall(1, 1), Wall(2, 1)}
    GRID = Grid(_board_rows, _board_columns, _start, _win_state, _lose_states, _blocked_cells, name='Grid3')


class Grid4:
    _board_rows = 4
    _board_columns = 4
    _win_state = {Goal(3, 0)}
    _lose_states = set()
    _start = Start(3, 2)
    _blocked_cells = {Wall(1, 1), Wall(2, 1), Wall(3, 1), Wall(0, 3), Wall(1, 3), Wall(2, 3), Wall(3, 3)}
    GRID = Grid(_board_rows, _board_columns, _start, _win_state, _lose_states, _blocked_cells, name='Grid4')


class Grid5:
    _board_rows = 4
    _board_columns = 4
    _win_state = {Goal(3, 0)}
    _lose_states = {SnakePit(1, 1),SnakePit(1, 3)}
    _start = Start(3, 2)
    _blocked_cells = {Wall(2, 1), Wall(3, 1), Wall(0, 3), Wall(2, 3), Wall(3, 3)}
    GRID = Grid(_board_rows, _board_columns, _start, _win_state, _lose_states, _blocked_cells, name='Grid5')


class Grid6:
    _board_rows = 5
    _board_columns = 5
    _win_state = {Goal(2, 0)}
    _lose_states = {SnakePit(1, 1)}
    _start = Start(1, 4)
    _blocked_cells = {Wall(0, 0), Wall(4, 1), Wall(2, 2), Wall(1, 3), Wall(3, 3)}
    GRID = Grid(_board_rows, _board_columns, _start, _win_state, _lose_states, _blocked_cells, name='Grid6')


class Grid7:
    _board_rows = 6
    _board_columns = 6
    _win_state = {Goal(5, 0)}
    _lose_states = {SnakePit(3, 1), SnakePit(1, 0)}
    _start = Start(0, 5)
    _blocked_cells = {Wall(1, 1), Wall(1, 2), Wall(1, 3), Wall(2, 3), Wall(2, 4), Wall(4, 2), Wall(5, 2), Wall(5, 3),
                      Wall(4, 3), Wall(5, 4)}
    GRID = Grid(_board_rows, _board_columns, _start, _win_state, _lose_states, _blocked_cells, name='Grid7')
