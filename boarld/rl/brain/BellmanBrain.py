import sys

import progressbar
from boarld.rl.brain.Brain import Brain
from boarld.rl.qtable.Qtable import Qtable
import numpy as np


class BellmanBrain(Brain):

    def learn(self, nb_episodes, nb_of_eps_before_table_update, qtable_convergence_threshold,
              nb_steps_before_timeout, random_rate=0.3, learning_rate=0.2, discount_factor=0.7):

        self.possible_states = self.agent.get_list_of_possible_states()
        print(len(self.possible_states))
        self.valueFunctionDict = {st: 0 for st in self.possible_states}

        for i in progressbar.progressbar(range(nb_episodes)):
            self.episode(nb_steps_before_timeout, random_rate, learning_rate, discount_factor)


        self.agent.Qtable = Qtable(set(self.agent.possible_actions))
        for state in self.possible_states:
            for action in self.agent.possible_actions:
                new_st = self.agent.get_new_state_after_action(state, action)
                value = self.valueFunctionDict[new_st]
                self.agent.Qtable.update_value(state, action, self.agent.get_reward(state, action) + discount_factor * np.round(value, 2))
        self.agent.Qtable.update_table_by_shadow()



    def episode(self, nb_steps_before_timeout, random_rate, learning_rate, discount_factor):
        RHStab = Qtable(set(self.agent.possible_actions))

        for st in self.possible_states:
            for ac in self.agent.possible_actions:
                val = discount_factor * self.valueFunctionDict[
                    self.agent.get_new_state_after_action(st, ac)] + self.agent.get_reward(st, ac)
                RHStab.update_value(st, ac, val)
                RHStab.update_table_by_shadow()

        for st in self.possible_states:
            self.valueFunctionDict[st] = RHStab.get_greedy_best_action(st)[1]


