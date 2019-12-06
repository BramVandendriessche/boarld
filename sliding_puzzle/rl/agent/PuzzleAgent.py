import random
import time
import json

from boarld.env.action.Action import *
from boarld.env.state.State import State
from boarld.rl.agent.Agent import Agent
from sliding_puzzle.env.board.SlidingPuzzle import SlidingPuzzle
from sliding_puzzle.env.state.State import PuzzleState


class PuzzleAgent(Agent):

    def __init__(self, board: SlidingPuzzle, step_reward=-1, goal_reward=1):
        super().__init__(board=board,
                         init_state=board.init_state,
                         final_states={PuzzleState(board.goal_sequence, (board.nb_rows -1, board.nb_cols -1))},
                         step_reward=step_reward,
                         goal_reward=goal_reward)

    def serialize(self):
        dic = {
            "nb_rows": self.board.nb_rows,
            "nb_cols": self.board.nb_cols,
            "state": self.current_state.data
        }

        return json.dumps(dic)

    def get_reward(self, state: State, action):
        if state.data == self.board.goal_sequence:
            return 0
        elif self.get_new_state_after_action(state, action).data == self.board.goal_sequence:
            return self.goal_reward
        else:
            return self.step_reward

    def state_is_final(self, st):
        return st.data == self.board.goal_sequence

    def move(self, action: Action):
        self.current_state = self.board.move(action)
        self.add_state_to_traveled_path(self.current_state)
        self.notify_observers_of_change()
        return self.current_state

    def get_new_state_after_action(self, current_state: PuzzleState, action: Action, move_from_absorbing_state_allowed: bool = False):
        if current_state.data != self.board.goal_sequence or move_from_absorbing_state_allowed:
            return self.board.get_new_state_after_action(current_state, action)
        return current_state

    def solve(self, delay=3):
        time.sleep(delay)
        if self.current_state in self.Qtable.possible_states:
            for ac in self.get_greedy_best_path_from_state_to_goal(self.current_state)[0]:
                self.move(ac)
            if self.state_is_final(self.current_state):
                print('Done!')
            else:
                print('Senseless movement..')
        else:
            print("Can't solve this one :(")

    def set_agent_to_random_state(self, **kwargs):
        self.board.set_puzzle_to_solution()
        self.current_state = self.board.puzzle_to_state()
        self.traveled_path = [self.current_state]
        self.notify_observers_of_change()
        self.shuffle_n_actions(kwargs['nb_actions'])

    def get_possible_actions(self, state=None, move_from_absorbing_state_allowed: bool=False):
        if state is not None:
            return [ac for (ac, st) in self.get_results_of_all_possible_actions(state, move_from_absorbing_state_allowed) if st.data != state.data]
        return super().get_possible_actions(state)

    def shuffle_n_actions(self, n: int = 100):
        for _ in range(n):
            possible_actions = self.get_possible_actions(self.current_state, True)
            new_action = possible_actions[random.randint(0, len(possible_actions) - 1)]
            self.move(new_action)

        self.board.init_state = self.board.puzzle_to_state()
        self.board.init_sequence = [v for sublist in self.board.init_state.data for v in sublist]
        self.init_state = self.board.init_state

    def get_list_of_possible_states(self):
        handled = set()
        unhandled = {self.init_state}
        while unhandled:
            st = unhandled.pop()
            for ac in self.possible_actions:
                new_st = self.get_new_state_after_action(st, ac, move_from_absorbing_state_allowed=True)
                if new_st not in handled and new_st not in unhandled and new_st.data != st.data:
                    unhandled.add(new_st)
            handled.add(st)
        return list(handled)
