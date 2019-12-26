from boarld.core.rl.arlgorithm.AbstractQlearningARLgorithm import AbstractQlearningARLgorithm


class SarsaARLgorithm(AbstractQlearningARLgorithm):
    """
    Implementation of SARSA (state, action, reward, state, action) algorithm.
    """

    def episode(self, steps_before_timeout, random_rate, learning_rate, discount_factor):
        stps = 0
        s1 = self.agent.current_state
        a1 = self.agent.choose_action_epsilon_greedily(random_rate, s1)
        while not self.agent.state_is_final(self.agent.current_state) and stps <= steps_before_timeout:
            stps += 1
            s2 = self.agent.move(a1)
            r = self.agent.get_reward(s1, a1)
            a2 = self.agent.choose_action_epsilon_greedily(random_rate, s1)
            p1 = self.agent.Qtable.get_Q_value(s1, a1, True)
            p2 = learning_rate * (r + discount_factor *
                                  self.agent.Qtable.get_Q_value(s2, a2, True) - self.agent.Qtable.get_Q_value(s1, a1, True))
            self.agent.Qtable.update_value(s1, a1, p1 + p2)
            s1 = s2
            a1 = a2
        self.agent.reset()
