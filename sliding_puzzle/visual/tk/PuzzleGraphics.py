import sys
import time

from boarld.util.observ.Observable import Observable
from boarld.util.observ.Observer import Observer
from sliding_puzzle.env.board.SlidingPuzzle import SlidingPuzzle
from sliding_puzzle.env.board import PuzzleCell

if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


class PuzzleGraphics(Observer):

    def __init__(self, puzzle: SlidingPuzzle, window_size=800):
        super().__init__()
        self.root = tk.Tk()
        self.puzzle = puzzle
        self.window_size = window_size
        self.unit = self.window_size / max(self.puzzle.nb_rows, self.puzzle.nb_cols)
        self.canvas = None
        self.cell_rectangles = {}
        self.number_grid = {}
        self.add_observable(puzzle)

        self.build()

    def build(self):
        if self.canvas is not None:
            self.canvas.destroy()
        self.canvas = tk.Canvas(self.root, height=min(self.unit * self.puzzle.nb_rows, self.window_size),
                                width=min(self.unit * self.puzzle.nb_cols, self.window_size))
        self.canvas.pack()
        # TODO: use lines instead of rectangles: ~2n instead of ~n^2
        for y in range(self.puzzle.nb_rows):
            for x in range(self.puzzle.nb_cols):
                color = self.map_celltype_to_color(self.puzzle.get_cell_at_position(x, y))
                self.cell_rectangles[(x, y)] = self.canvas.create_rectangle(x * self.unit, y * self.unit,
                                                                            (x + 1) * self.unit, (y + 1) * self.unit,
                                                                            width=8, fill=color)
                self.number_grid[(x, y)] = self.canvas.create_text(x * self.unit + self.unit / 2, y * self.unit + self.unit / 2,
                                        text=str(self.puzzle.get_cell_at_position(x, y).value), font=("Courier", 100))

    def map_celltype_to_color(self, cell: PuzzleCell):
        if cell.value == 0:
            return 'red'
        return 'white'

    def mainloop(self):
        self.root.mainloop()

    def act_on_notify(self, observable: Observable):
        if self.puzzle==observable:
            for cell in self.puzzle.cell_set:
                self.canvas.itemconfigure(self.number_grid[(cell.x, cell.y)], text=cell.value)
                self.canvas.itemconfigure(self.cell_rectangles[(cell.x, cell.y)], fill=self.map_celltype_to_color(cell))
            time.sleep(2)


