import random
from abc import ABC, abstractmethod
from typing import List, Set

from boarld.env.action.Action import *
from boarld.env.board.Board import Board
from boarld.env.state.State import State
from boarld.rl.qtable.Qtable import Qtable
from boarld.util.observ.Observable import Observable


class Agent(Observable, ABC):

    def __init__(self, board: Board, init_state: State, final_states: Set[State], step_reward=-2, goal_reward=10):
        super().__init__()
        self.board = board
        self.init_state = init_state
        self.final_states = final_states
        self.current_state = init_state
        self.step_reward = step_reward
        self.goal_reward = goal_reward
        self.possible_actions: List[Action.__class__] = [Up, Down, Left, Right]
        self.Qtable: Qtable = Qtable(set(self.get_possible_actions()))
        for final_state in final_states:
            for ac in self.possible_actions:
                self.Qtable.update_value(final_state, ac, self.Qtable.default_value)
        self.Qtable.update_table_by_shadow()
        self.traveled_path = [self.current_state]

    @abstractmethod
    def get_reward(self, state: State):
        pass

    @abstractmethod
    def state_is_final(self, st):
        pass

    @abstractmethod
    def move(self, action: Action):
        pass

    @abstractmethod
    def get_new_state_after_action(self, current_state: State, action: Action):
        pass

    @abstractmethod
    def set_agent_to_random_state(self, **kwargs):
        pass

    # By default, return all possible actions; to be overridden by child when required.
    def get_possible_actions(self, state=None):
        return self.possible_actions

    def learn(self, brain, nb_episodes, nb_of_eps_before_table_update, qtable_convergence_threshold,
              nb_steps_before_timeout, random_rate, learning_rate, discount_factor):
        brain(self).learn(nb_episodes, nb_of_eps_before_table_update, qtable_convergence_threshold,
                          nb_steps_before_timeout, random_rate, learning_rate, discount_factor)

    def get_results_of_all_possible_actions(self, state):
        return [(a, self.get_new_state_after_action(state, a))
                for a in self.get_possible_actions()]

    def reset(self):
        self.board.reset()
        self.current_state = self.init_state
        self.traveled_path = [self.current_state]
        self.notify_observers_of_change()

    def choose_action_epsilon_greedily(self, epsilon, state: State):
        if random.random() < epsilon:
            return self.get_possible_actions(state)[random.randint(0, len(self.get_possible_actions(state)) - 1)]
        else:
            return self.Qtable.get_greedy_best_action(state, self.get_possible_actions(state))[0]

    def get_greedy_best_path_from_state_to_goal(self, state):

        path = [state]
        actions = []
        st = state
        while True:
            action = self.Qtable.get_greedy_best_action(st)[0]
            actions.append(action)
            st = self.get_new_state_after_action(st, action)
            if st in path:
                break
            path.append(st)
            if self.state_is_final(st):
                break
        return actions, path

    def add_state_to_traveled_path(self, state):
        if self.traveled_path[-1] != state:
            self.traveled_path.append(state)
