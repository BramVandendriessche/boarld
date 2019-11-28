import numpy as np

from gridworld.rl.agent.GridAgent import GridAgent
from gridworld.env.board.Grid import Grid


class BellmanAgent(GridAgent):
    def __init__(self, board: Grid, step_reward=-2, goal_reward=10, snakepit_reward=-10, learning_rate=0.5,
                 discount_factor=0.7):
        super().__init__(board, step_reward, goal_reward, snakepit_reward, 0, learning_rate, discount_factor)

    def learn(self, nb_episodes):

        nb_elems = self.board.nb_cols * self.board.nb_rows

        I = np.identity(nb_elems)
        P = np.zeros((nb_elems, nb_elems))
        r = np.zeros((nb_elems, len(self.possible_actions)))

        for y in range(self.board.nb_rows):
            for x in range(self.board.nb_cols):
                neighbors = self.get_results_of_all_possible_actions(self.map_cell_to_state(self.board.get_cell_at_position(x, y)))
                for a, neighbor in neighbors:
                    P[y * self.board.nb_cols + x][neighbor.data.y * self.board.nb_cols + neighbor.data.x] += 1 / len(neighbors)
                    r[y * self.board.nb_cols + x][self.possible_actions.index(a)] = self.get_reward(neighbor)

        q = np.dot(np.linalg.inv(I - self.discount_factor * P), r)

        for cell in self.board.cell_set:
            state = self.map_cell_to_state(cell)
            for idx, action in enumerate(self.possible_actions):
                self.Qtable.update_value(state, action, q[cell.y * self.board.nb_cols + cell.x][idx])


