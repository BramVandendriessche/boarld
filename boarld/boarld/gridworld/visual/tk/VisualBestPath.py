from boarld.gridworld.rl.agent.GridAgent import GridAgent
from boarld.gridworld.visual import AbstractVisualGrid
from boarld.core.util.observ.Observable import Observable
from boarld.core.util.observ.Observer import Observer


class VisualBestPath(AbstractVisualGrid, Observer):

    def __init__(self, agent: GridAgent):
        self.agent: GridAgent = agent
        super().__init__(agent.board)
        self.add_observable(agent.Qtable)

    def act_on_notify(self, observable: Observable):

        _, path = self.agent.get_greedy_best_path_from_state_to_goal(self.agent.init_state)
        for y in range(self.grid.nb_rows):
            for x in range(self.grid.nb_cols):
                color = self.map_celltype_to_color(self.grid.get_cell_at_position(x, y))
                if self.agent.map_cell_to_state(self.grid.get_cell_at_position(x, y)) in path:
                    color = 'blue'
                self.canvas.itemconfig(self.cell_rectangles[(x, y)], fill=color)

        # time.sleep(.5)
