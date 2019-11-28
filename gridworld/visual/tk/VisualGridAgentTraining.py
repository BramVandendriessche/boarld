from gridworld.rl.agent.GridAgent import GridAgent
from gridworld.visual.tk.AbstractVisualGrid import AbstractVisualGrid
from boarld.util.observ.Observable import Observable
from boarld.util.observ.Observer import Observer


class VisualGridAgentTraining(AbstractVisualGrid, Observer):

    def __init__(self, agent: GridAgent):
        self.agent: GridAgent = agent
        super().__init__(agent.board)
        self.add_observable(agent)
        self.path_circles = {}
        self.path_lines = {}

    def act_on_notify(self, observable: Observable):

        tuples = [(s.data.x, s.data.y) for s in self.agent.traveled_path]

        for y in range(self.grid.nb_rows):
            for x in range(self.grid.nb_cols):
                key = (x, y)
                if key in tuples:
                    if key not in self.path_circles:
                        self.path_circles[key] = self.canvas.create_oval(x * self.unit + self.unit/2 - self.unit / 10, y * self.unit + self.unit/2 - self.unit / 10, x * self.unit + self.unit/2 + self.unit / 10, y * self.unit + self.unit/2 + self.unit / 10, width=2)
                    else:
                        self.canvas.itemconfig(self.path_circles[key], fill='white')
                    if key == tuples[len(tuples)-1]:
                        self.canvas.itemconfig(self.path_circles[key], fill='orange')
                else:
                    if key in self.path_circles:
                        self.canvas.delete(self.path_circles.pop(key))

        line_keys = set()
        for idx, tuple in enumerate(tuples[:-1]):
            x, y = tuple
            x2, y2 = tuples[idx+1]
            line_coor = (x, y, x2, y2)
            if line_coor not in self.path_lines:
                self.path_lines[line_coor] = self.canvas.create_line(x * self.unit + self.unit / 2, y * self.unit + self.unit / 2, x2 * self.unit + self.unit / 2, y2 * self.unit + self.unit / 2)
            line_keys.add(line_coor)
        for line_key in list(self.path_lines.keys()):
            if line_key not in line_keys:
                self.canvas.delete(self.path_lines.pop(line_key))

        # time.sleep(.5)
