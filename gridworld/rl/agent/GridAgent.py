import random
from typing import Dict

from boarld.env.action.Action import *
from boarld.env.state.State import State
from boarld.rl.agent.Agent import Agent
from gridworld.env.board import Grid
from gridworld.env.board.GridCell import *
from gridworld.env.state.State import GridState


class GridAgent(Agent):
    def __init__(self, board: Grid,
                 step_reward=-1, goal_reward=10, snakepit_reward=-10,):
        self.possible_states: Dict[GridCell, State] = {c: GridState(c) for c in board.cell_set}
        self.possible_init_positions = [cell for cell in board.cell_set if not isinstance(cell, Goal) and not isinstance(cell, Wall) and not isinstance(cell, SnakePit)]
        super().__init__(board=board, init_state=self.possible_states[board.start], final_states={st for st in self.possible_states.values() if st.data not in self.possible_init_positions}, step_reward=step_reward,
                         goal_reward=goal_reward)

        self.snakepit_reward = snakepit_reward

    def get_reward(self, state: State):
        if isinstance(state.data, Goal):
            return self.goal_reward
        elif isinstance(state.data, SnakePit):
            return self.snakepit_reward
        else:
            return self.step_reward  # TODO: bigger penalty if stays in same state?

    def state_is_final(self, st):
        return isinstance(st.data, Goal) or isinstance(st.data, SnakePit)

    def move(self, action: Action):
        self.current_state = self.get_new_state_after_action(self.current_state, action)
        self.add_state_to_traveled_path(self.current_state)
        self.notify_observers_of_change()
        return self.current_state

    def get_new_state_after_action(self, current_state: State, action: Action) -> State:
        new_state = current_state
        if action == Up:
            new_state = self.map_cell_to_state(self.board.cells[max(0, current_state.data.y - 1)][current_state.data.x])
        elif action == Down:
            new_state = self.map_cell_to_state(
                self.board.cells[min(self.board.nb_rows - 1, current_state.data.y + 1)][current_state.data.x])
        elif action == Left:
            new_state = self.map_cell_to_state(self.board.cells[current_state.data.y][max(0, current_state.data.x - 1)])
        elif action == Right:
            new_state = self.map_cell_to_state(
                self.board.cells[current_state.data.y][min(self.board.nb_cols - 1, current_state.data.x + 1)])
        if isinstance(new_state.data, Wall):
            return current_state
        return new_state

    def map_cell_to_state(self, cell: GridCell):
        return self.possible_states[cell]

    def set_agent_to_random_state(self, **kwargs):
        self.current_state = self.possible_states[self.possible_init_positions[random.randint(0, len(self.possible_init_positions)-1)]]
        self.traveled_path = [self.current_state]
        self.notify_observers_of_change()
        return self.current_state
