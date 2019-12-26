import random

from boarld.core.rl.arlgorithm.AbstractQlearningARLgorithm import AbstractQlearningARLgorithm


class DynaQARLgorithm(AbstractQlearningARLgorithm):
    """
    Implementation of Dyna-Q.
    """

    def episode(self, steps_before_timeout, random_rate, learning_rate, discount_factor):
        stps = 0

        while not self.agent.state_is_final(self.agent.current_state) and stps <= steps_before_timeout:
            stps += 1
            old_state = self.agent.current_state
            next_action = self.agent.choose_action_epsilon_greedily(random_rate, old_state)

            self.agent.move(next_action)
            if not self.agent.state_is_final(self.agent.current_state):
                self.agent.Qtable.update_value(old_state, next_action,
                                               self.get_new_value(discount_factor, learning_rate, next_action, old_state))

            else:
                self.agent.Qtable.update_value(old_state, next_action,
                                               self.agent.get_reward(old_state, next_action))

            self.agent.Qtable.update_table_by_shadow()
            n_steps = 10
            poss_states = tuple(self.agent.Qtable.possible_states)
            for _ in range(n_steps):
                random_state = random.choice(poss_states)
                random_action = random.choice(tuple(self.agent.get_possible_actions(random_state)))
                self.agent.Qtable.update_value(random_state, random_action,
                                               self.get_new_value(discount_factor, learning_rate, random_action, random_state))
                self.agent.Qtable.update_table_by_shadow()


        self.agent.reset()

    def get_new_value(self, discount_factor, learning_rate, next_action, old_state):
        p1 = (1 - learning_rate) * self.agent.Qtable.get_Q_value(old_state, next_action, True)
        p2 = learning_rate * (self.agent.get_reward(old_state, next_action) + discount_factor *
                              self.agent.Qtable.get_greedy_best_action(self.agent.current_state)[1])
        return p1 + p2
