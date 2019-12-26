import random
from abc import ABC, abstractmethod
from typing import List, Set

from boarld.core.env.action.Action import *
from boarld.core.env.board.Board import Board
from boarld.core.env.state.State import State
from boarld.core.rl.qtable.Qtable import Qtable
from boarld.core.util.observ.JsonObservable import JsonObservable


class Agent(JsonObservable, ABC):
    """
    Class representing a reinforcement learning agent. The agent contains a board on which it operates, a current state
    and one or more target states, receives a reward for performing a move and reaching a target state.
    """

    def __init__(self, board: Board, init_state: State, final_states: Set[State], step_reward: float = -2, goal_reward:float =10):
        """
        Construct an Agent with a given Board on which it should operate, an initial state, a set of final states and
        rewards for performing an action and reaching the target state.
        :param board: The Board on which the agent operates.
        :param init_state: The agent's initial State
        :param final_states: A set of States considered final, which the agent should try to reach.
        :param step_reward: The reward received by the agent upon performing an Action.
        :param goal_reward: The reward received by the agent upon reaching the target state.
        """
        super().__init__()
        self.board = board
        self.init_state = init_state
        self.final_states = final_states
        self.current_state = init_state
        self.step_reward = step_reward
        self.goal_reward = goal_reward
        self.possible_actions: List[Action] = [Up(), Down(), Left(), Right()]
        self.Qtable: Qtable = Qtable(set(self.get_possible_actions()))
        for final_state in final_states:
            for ac in self.possible_actions:
                self.Qtable.update_value(final_state, ac, self.Qtable.default_value)
        self.Qtable.update_table_by_shadow()
        self.traveled_path = [self.current_state]

    @abstractmethod
    def get_reward(self, state: State, action: Action):
        """
        Get the reward received by the agent for performing the given action in the given state.
        :param state: The state in which the agent would perform the given action.
        :param action: The action performed by the agent in the given state.
        :return: The reward received by the agent for performing the given action in the given state.
        """
        pass

    @abstractmethod
    def state_is_final(self, state: State):
        """
        Return if the given state is a final state. Not that a state being final does not necessarily mean that the state is
        a target state!
        :param state: The given state, of which should be determined if it is final.
        :return: True when the given State is final, else False.
        """
        pass

    @abstractmethod
    def move(self, action: Action):
        """
        Make the agent perform a given Action.
        :param action: The action to be performed by the Agent.
        :return: None
        """
        pass

    @abstractmethod
    def get_new_state_after_action(self, current_state: State, action: Action,
                                   move_from_absorbing_state_allowed: bool = False):
        """
        Get the state resulting from performing the given action in the given state. If moving from an absorbing state is
        allowed, the state resulting from moving in an absorbing state, is possibly a neighboring state. Else, moving
        in an absorbing state results in a status quo. This is particularly useful for discovering states possible states.
        :param current_state: The state in which the given action is performed.
        :param action: The action performed.
        :param move_from_absorbing_state_allowed: Is moving from an absorbing state (e.g. a target state),
        allowed? False by default.
        :return: The state resulting from performing the given action in the given state.
        """
        pass

    @abstractmethod
    def set_agent_to_random_state(self, **kwargs):
        """
        Set the agent to a random state. For more information, take a look at concrete implementations.
        """
        pass

    @abstractmethod
    def get_list_of_possible_states(self):
        """
        Get all the agent's possible states.
        :return: A list of the possible states the agent can be in.
        """
        pass

    def solve(self):
        """
        Perform the actions required to reach the best possible state. When the agent has been trained, it is able to
        end up in a/the target state. Else, it will perform the actions considered best at the time.
        :return:
        """
        for ac in self.get_greedy_best_path_from_state_to_goal(self.current_state)[0]:
            self.move(ac)

    def get_possible_actions(self, state=None, move_from_absorbing_state_allowed: bool = False):
        """
        Return all possible actions in a given state.
        :param state: The state in which we want to obtain all possible action.
        :param move_from_absorbing_state_allowed: Is moving from an absorbing state (e.g. a target state),
        allowed? False by default.
        :return: A list of all actions that can be performed in the given state.
        """
        return self.possible_actions

    def learn(self, arlgorithm, nb_episodes, nb_of_eps_before_table_update, qtable_convergence_threshold,
              nb_steps_before_timeout, random_rate, learning_rate, discount_factor):
        """
        Train the agent using the given algorithm (the ARLgorithm) and hyperparameters. This process results in
        an updated Q-table.
        :param arlgorithm: The ARLgorithm, containing the algorithm used to train the agent.
        :param nb_episodes: The number of episodes to be trained.
        :param nb_of_eps_before_table_update: The number of episodes before the Qtable is updated by its shadow.
        :param qtable_convergence_threshold: The threshold below which the Qtable is considered to have converged.
        Convergence is defined between the Qtable and a snapshot as follows:
        max({abs(Qvalue(state, action) - snapshot(state, action) for each (state, action)})
        :param nb_steps_before_timeout: The number of steps the agent is allowed to perform before the episode is terminated.
        :param random_rate: Epsilon for epsilon-greedy action selection: the best action is selected with a probability of
        (1-random_rate), a random action is selected with a random_rate probability.
        :param learning_rate: The learning rate (alpha) determines to what extent newly acquired information should
        be incorporated in the agent's knowledge. A learning rate of 0 yields in zero learning, a value of 1 makes the
        agent only use the newest information.
        :param discount_factor: The discount factor (gamma) determines the importance of future rewards: A discount
        factor of 0 makes the agent only consider current rewards, a value close to 1 makes it aim for long-term rewards.
        :return: None
        """
        arlgorithm(self).learn(nb_episodes, nb_of_eps_before_table_update, qtable_convergence_threshold,
                          nb_steps_before_timeout, random_rate, learning_rate, discount_factor)

    def get_results_of_all_possible_actions(self, state, move_from_absorbing_state_allowed: bool=False):
        """
        Get all states that can result from performing the actions possible in the given state. If moving from an
        absorbing state is allowed, the state resulting from moving in an absorbing state, is possibly a neighboring
        state. Else, moving in an absorbing state results in a status quo.
        :param state: The state of which all "neighboring" states should be calculated.
        :param move_from_absorbing_state_allowed: Is moving from an absorbing state (e.g. a target state),
        allowed? False by default.
        :return: A list of all possible states resulting from performing the possible actions in the given state.
        """
        return [(action, self.get_new_state_after_action(state, action, move_from_absorbing_state_allowed=move_from_absorbing_state_allowed))
                for action in self.get_possible_actions()]

    def reset(self):
        """
        Reset the agent to the initial state, clear the path traveled by the agent, reset the board.
        :return: None
        """
        self.board.reset()
        self.current_state = self.init_state
        self.traveled_path = [self.current_state]
        self.notify_observers_of_change()

    def choose_action_epsilon_greedily(self, epsilon: float, state: State):
        """
        Get an action epsilon-greedily: the best action is selected with a probability of
        (1-random_rate), a random action is selected with a random_rate probability.
        :param epsilon: The probability with which a random action should be selected.
        :param state: The state in which the chosen action should be performed. Note that only actions allowed in
        the given state are considered.
        :return: A random action with a probability of epsilon, or the best action according to the agent's current knowledge.
        """
        if random.random() < epsilon:
            acts = self.get_possible_actions(state)
            if len(acts) == 0:
                return None
            return acts[random.randint(0, len(acts) - 1)]
        else:
            return self.Qtable.get_greedy_best_action(state, self.get_possible_actions(state))[0]

    def get_greedy_best_path_from_state_to_goal(self, state):
        """
        Get the best path from the given state. If the agent is trained, this path ends in a target state. The search
        process is terminated if the agent would travel an infinite (circular) path. If multiple actions are equally
        valuable in a certain state, one is chosen randomly.
        :param state: The state from which the path is to be calculated.
        :return: The best path starting from the given state. This path might end in a target state, but this is not
        necessarily the case.
        """
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

    def _add_state_to_traveled_path(self, state):
        """
        Add the given state to the agent's currently traveled path.
        :param state: The given state to be added to the agent's traveled path.
        :return: None
        """
        if self.traveled_path[-1] != state:
            self.traveled_path.append(state)
