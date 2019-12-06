import random
from typing import Dict
import json

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

    def get_reward(self, state: State, action: Action):
        if isinstance(state.data, (Goal, SnakePit, Wall)):
            return 0
        new_state = self.get_new_state_after_action(state, action)
        if isinstance(new_state.data, Goal):
            return self.goal_reward
        elif isinstance(new_state.data, SnakePit):
            return self.snakepit_reward
        else:
            return self.step_reward  # TODO: bigger penalty if stays in same state?

    def state_is_final(self, st):
        return isinstance(st.data, (Goal, SnakePit))

    def move(self, action: Action):
        self.current_state = self.get_new_state_after_action(self.current_state, action)
        self.add_state_to_traveled_path(self.current_state)
        self.notify_observers_of_change()
        return self.current_state

    def get_new_state_after_action(self, current_state: State, action: Action, move_from_absorbing_state_allowed: bool = False) -> State:
        new_state = current_state
        if (not move_from_absorbing_state_allowed) and (isinstance(current_state.data, (Goal, SnakePit))) \
                or isinstance(current_state.data, Wall):
            pass
        elif action == Up:
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

    def get_list_of_possible_states(self):
        return list(self.possible_states.values())

    def serialize(self):
        dic = {
            "board_setup": {
                "nb_rows": self.board.nb_rows,
                "nb_cols": self.board.nb_cols,
                "holes": [[x + 1, y + 1] for x, y in self.board.snake_pits.keys()],
                "obstacles": [[x + 1, y + 1] for x, y in self.board.walls.keys()],
                "footsteps": [[st.data.x + 1, st.data.y + 1] for st in self.traveled_path],
                "start": [self.init_state.data.x + 1, self.init_state.data.y + 1],
                "end": [[x + 1, y + 1] for x,y in self.board.goals]
            },
            "best_path_now": [[st.data.x+1, st.data.y+1] for st in
                              self.get_greedy_best_path_from_state_to_goal(self.init_state)[1]],
            "best_actions": [
                {"x": cell.x + 1, "y": cell.y + 1,
                 "actions": [ac.to_string() for ac,_ in self.Qtable.get_list_of_greedy_best_actions(self.map_cell_to_state(cell))]}
                for cell in self.board.cell_set if not isinstance(cell, (Wall, SnakePit, Goal))
            ]

        }
        return json.dumps(dic)
