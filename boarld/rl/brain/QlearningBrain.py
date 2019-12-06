from boarld.rl.brain.Brain import Brain


class QlearningBrain(Brain):

    def episode(self, steps_before_timeout, random_rate, learning_rate, discount_factor):
        stps = 0

        while not self.agent.state_is_final(self.agent.current_state) and stps <= steps_before_timeout:
            stps += 1
            old_state = self.agent.current_state
            next_action = self.agent.choose_action_epsilon_greedily(random_rate, old_state)

            self.agent.move(next_action)
            if not self.agent.state_is_final(self.agent.current_state):
                self.agent.Qtable.update_value(old_state, next_action,
                                               self.get_new_q_value(old_state, self.agent.current_state,
                                                                    next_action, learning_rate, discount_factor))

            else:
                self.agent.Qtable.update_value(old_state, next_action,
                                               self.agent.get_reward(old_state, next_action))
        self.agent.reset()

    def get_new_q_value(self, old_state, new_state, next_action, learning_rate, discount_factor):
        p1 = (1 - learning_rate) * self.agent.Qtable.get_Q_value(old_state, next_action, True)
        p2 = learning_rate * (self.agent.get_reward(old_state, next_action) + discount_factor *
                              self.agent.Qtable.get_greedy_best_action(new_state)[1])
        return p1 + p2
