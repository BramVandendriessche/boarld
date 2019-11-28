import random
import time

from boarld.env.action.Action import *
from boarld.env.state.State import State
from boarld.rl.agent.Agent import Agent
from sliding_puzzle.env.board.SlidingPuzzle import SlidingPuzzle
from sliding_puzzle.env.state.State import PuzzleState


class PuzzleAgent(Agent):
    def __init__(self, board: SlidingPuzzle, step_reward=-1,
                 goal_reward=1):
        super().__init__(board=board, init_state=board.init_state, final_states={PuzzleState(board.goal_sequence, (board.nb_rows, board.nb_cols))}, step_reward=step_reward, goal_reward=goal_reward)

    def get_reward(self, state: State):
        if state.data == self.board.goal_sequence:
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

    def get_new_state_after_action(self, current_state: PuzzleState, action: Action):
        return self.board.get_new_state_after_action(current_state, action)

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

    def get_possible_actions(self, state=None):
        if state is not None:
            return [ac for (ac, st) in self.get_results_of_all_possible_actions(state) if st.data != state.data]
        return super().get_possible_actions(state)

    def shuffle_n_actions(self, n: int = 100):
        for _ in range(n):
            new_action = self.possible_actions[random.randint(0, len(self.possible_actions) - 1)]
            self.move(new_action)

        self.board.init_state = self.board.puzzle_to_state()
        self.board.init_sequence = [v for sublist in self.board.init_state.data for v in sublist]
        self.init_state = self.board.init_state
