from abc import ABC, abstractmethod
import progressbar

from boarld.rl.agent.Agent import Agent


class Brain(ABC):
    def __init__(self, agent):
        self.agent: Agent = agent

    @abstractmethod
    def learn(self, nb_episodes, nb_of_eps_before_table_update, qtable_convergence_threshold,
              nb_steps_before_timeout, random_rate=0.3, learning_rate=0.2, discount_factor=0.7): pass
