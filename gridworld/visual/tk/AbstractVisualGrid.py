import sys

from gridworld.env.board.GridCell import Goal, Start, SnakePit, Wall
from gridworld.env.board.Grid import Grid
from boarld.util.observ.Observer import Observer

if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


class AbstractVisualGrid(Observer):
    def __init__(self, grid: Grid, window_size=800):
        super().__init__()
        self.root = tk.Tk()
        self.grid = grid
        self.window_size = window_size
        self.unit = self.window_size / max(self.grid.nb_rows, self.grid.nb_cols)
        self.canvas = None
        self.cell_rectangles = {}

        self.build()

    def build(self):
        if self.canvas is not None:
            self.canvas.destroy()
        self.canvas = tk.Canvas(self.root, height=min(self.unit * self.grid.nb_rows, self.window_size),
                           width=min(self.unit * self.grid.nb_cols, self.window_size))
        self.canvas.pack()
        # TODO: use lines instead of rectangles: ~2n instead of ~n^2
        for y in range(self.grid.nb_rows):
            for x in range(self.grid.nb_cols):
                color = self.map_celltype_to_color(self.grid.get_cell_at_position(x, y))

                self.cell_rectangles[(x, y)] = self.canvas.create_rectangle(x * self.unit, y * self.unit, (x + 1) * self.unit, (y + 1) * self.unit,
                                                                            width=8, fill=color)
                if isinstance(self.grid.get_cell_at_position(x, y), Goal):
                    self.create_finish(self.canvas, x * self.unit, y * self.unit)

    def map_celltype_to_color(self, cell):
        if isinstance(cell, Start):
            return 'green'
        elif isinstance(cell, SnakePit):
            return 'red'
        elif isinstance(cell, Wall):
            return 'black'
        return 'white'

    def create_finish(self, canvas, pos_x, pos_y):
        finish_unit = self.unit / 4
        color = 'white'
        switch_color = lambda: 'black' if color == 'white' else 'white'

        for i in range(4):
            color = switch_color()
            for j in range(4):
                color = switch_color()
                canvas.create_rectangle(pos_x + i * finish_unit, pos_y + j * finish_unit, pos_x + (i + 1) * finish_unit,
                                        pos_y + (j + 1) * finish_unit, width=1, fill=color)

    def mainloop(self):
        self.root.mainloop()
