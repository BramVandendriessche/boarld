from abc import ABC, abstractmethod
import progressbar

from boarld.rl.agent.Agent import Agent


class Brain(ABC):
    def __init__(self, agent):
        self.agent: Agent = agent

    @abstractmethod
    def episode(self, nb_steps_before_timeout, random_rate, learning_rate, discount_factor): pass

    def learn(self, nb_episodes, nb_of_eps_before_table_update, qtable_convergence_threshold,
              nb_steps_before_timeout, random_rate=0.3, learning_rate=0.2, discount_factor=0.7):
        table_counter = 0
        for i in progressbar.progressbar(range(nb_episodes)):
            if table_counter >= nb_of_eps_before_table_update or self.agent.Qtable.has_converged_since_last_snapshot(qtable_convergence_threshold):
                self.agent.Qtable.update_table_by_shadow()
                table_counter = 0
            else:
                self.agent.Qtable.take_snapshot()
            table_counter += 1
            self.agent.set_agent_to_random_state(nb_actions=min(max(int(i / 10), 1), 101))
            self.episode(nb_steps_before_timeout, random_rate, learning_rate, discount_factor)
        print('Done learning!')
