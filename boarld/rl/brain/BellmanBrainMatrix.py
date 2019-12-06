import numpy as np
import progressbar
from boarld.rl.brain.Brain import Brain


class BellmanBrainMatrix(Brain):

    def __init__(self, agent):
        super().__init__(agent)
        self.possible_states = self.agent.get_list_of_possible_states()
        self.valueFunction = {st: 0 for st in self.possible_states}
        self.nb_actions = len(self.agent.possible_actions)
        self.nb_states = len(self.possible_states)
        self.T = np.zeros((self.nb_states, self.nb_states, self.nb_actions))
        self.Reward = self.agent.step_reward * np.ones((self.nb_states, self.nb_actions))
        self.valueFunction = np.zeros((self.nb_states,))

    def learn(self, nb_episodes, nb_of_eps_before_table_update, qtable_convergence_threshold,
              nb_steps_before_timeout, random_rate=0.3, learning_rate=0.2, discount_factor=0.7):

        for stidx, st in enumerate(self.possible_states):
            for ac, new_st in self.agent.get_results_of_all_possible_actions(st):
                acidx = self.agent.possible_actions.index(ac)
                newstidx = self.possible_states.index(new_st)

                self.T[stidx, newstidx, acidx] = 1
                self.Reward[stidx, acidx] = self.agent.get_reward(st, ac)

        for _ in progressbar.progressbar(range(nb_episodes)):
            self.episode(discount_factor)

        for stidx, st in enumerate(self.possible_states):
            for acidx, ac in enumerate(self.agent.possible_actions):
                new_st = self.agent.get_new_state_after_action(st, ac)
                newstidx = self.possible_states.index(new_st)
                value = self.valueFunction[newstidx]
                self.agent.Qtable.update_value(st, ac, self.Reward[stidx, acidx] + discount_factor * np.round(value, 2))
        self.agent.Qtable.update_table_by_shadow()

    def episode(self, discount_factor):
        RHS = np.zeros((self.nb_states, self.nb_actions))
        for acidx, action in enumerate(self.agent.possible_actions):
            RHS[:, acidx] = discount_factor \
                            * np.dot(self.T[:, :, acidx], self.valueFunction).reshape((self.nb_states,)) \
                            + self.Reward[:, acidx]
        self.valueFunction = np.max(RHS, axis=1)
