from abc import ABC, abstractmethod

from boarld.core.rl.agent.Agent import Agent


class ARLgorithm(ABC):
    """
    Abstraction of a reinforcement learning arlgorithm, able to learn a policy that yields an agent a good reward.
    """
    def __init__(self, agent):
        """
        Construct ARLgorithm with a given agent.
        :param agent: The given agent, to which the arlgorithm belongs.
        """
        self.agent: Agent = agent

    @abstractmethod
    def learn(self, nb_episodes, nb_of_eps_before_table_update, qtable_convergence_threshold,
              nb_steps_before_timeout, random_rate=0.3, learning_rate=0.2, discount_factor=0.7):
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
        pass
