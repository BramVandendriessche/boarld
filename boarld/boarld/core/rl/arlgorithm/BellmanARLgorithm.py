import numpy as np
import progressbar
from boarld.core.rl.arlgorithm.ARLgorithm import ARLgorithm
from boarld.core.rl.qtable.Qtable import Qtable


class BellmanARLgorithm(ARLgorithm):
    """
    Implementation of reinfocement learning using the Bellman equations.
    """
    def __init__(self, agent):
        super().__init__(agent)
        self.possible_states = self.agent.get_list_of_possible_states()
        self.valueFunctionDict = {st: 0 for st in self.possible_states}

    def learn(self, nb_episodes, nb_of_eps_before_table_update, qtable_convergence_threshold,
              nb_steps_before_timeout, random_rate=0.3, learning_rate=0.2, discount_factor=0.7):

        for _ in progressbar.progressbar(range(nb_episodes)):
            self.iteration(discount_factor)

        for state in self.possible_states:
            for action in self.agent.possible_actions:
                new_st = self.agent.get_new_state_after_action(state, action)
                v = self.agent.get_reward(state, action) + discount_factor * np.round(self.valueFunctionDict[new_st], 2)
                self.agent.Qtable.update_value(state, action, v)
        self.agent.Qtable.update_table_by_shadow()

    def iteration(self, discount_factor):
        """
        Defines one iteration in the training process.
        :param discount_factor: The discount factor (gamma) determines the importance of future rewards: A discount
        factor of 0 makes the agent only consider current rewards, a value close to 1 makes it aim for long-term rewards.
        :return: None
        """
        RHStab = Qtable(set(self.agent.possible_actions))

        for st in self.possible_states:
            for ac in self.agent.possible_actions:
                val = discount_factor * self.valueFunctionDict[
                    self.agent.get_new_state_after_action(st, ac)] + self.agent.get_reward(st, ac)
                RHStab.update_value(st, ac, val)
                RHStab.update_table_by_shadow()

        for st in self.possible_states:
            self.valueFunctionDict[st] = RHStab.get_greedy_best_action(st)[1]
