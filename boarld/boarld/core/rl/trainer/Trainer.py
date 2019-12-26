from typing import Type

from boarld.core.rl.agent.Agent import Agent
from boarld.core.rl.arlgorithm.AbstractQlearningARLgorithm import AbstractQlearningARLgorithm
from boarld.core.rl.arlgorithm.BellmanARLgorithm import BellmanARLgorithm
from boarld.core.util.mqtt_params import mqtt_params
from boarld.core.visual.json.JsonObserver import JsonObserver
from paho.mqtt.client import Client


class Trainer:
    """
    Wrapper for training an agent using a certain algorithm (ARLgorithm), with the configured hyperparameters.
    """

    def __init__(self):
        self.observe_qtable = False
        self.observe_agent = False
        self.export_qtable = False
        self.arlgorithm = None
        self.nb_episodes = None
        self.nb_of_eps_before_table_update = None
        self.qtable_convergence_threshold = None
        self.nb_steps_before_timeout = None
        self.random_rate = None
        self.learning_rate = None
        self.discount_factor = None
        self.agent = None

    def train(self):
        """
        Train the given agent using the configured hyperparameters. All parameters are required, unless Bellman is used.
        In that case, one should only configure "discount_factor" and "nb_episodes", apart from the arlgorithm and the agent.
        :return: None
        """
        self._verify_hyperparameters()

        if self.observe_agent or self.observe_qtable:
            client = Client('main', transport='websockets')
            client.connect(mqtt_params.MQTT_HOST, mqtt_params.MQTT_PORT)
            observer = JsonObserver(client)

            if self.observe_qtable:
                observer.add_observable(self.agent.Qtable)
            if self.observe_agent:
                observer.add_observable(self.agent)
        args = \
            (self.arlgorithm, self.nb_episodes, self.nb_of_eps_before_table_update, self.qtable_convergence_threshold,
             self.nb_steps_before_timeout, self.random_rate, self.learning_rate, self.discount_factor)
        self.agent.learn(*args)

        if self.export_qtable:
            self.agent.Qtable.to_file(
                '%s_%s_%s_episodes.p' % (self.agent.board.name, self.arlgorithm.__name__, self.nb_episodes))

    def with_observe_qtable(self, observe_qtable):
        """
        Set whether the Qtable should be observable through a JsonObserver.
        :param observe_qtable: Indicator of whether the Qtable should be observable through a JsonObserver.
        :return: self
        """
        self.observe_qtable = observe_qtable
        return self

    def with_observe_agent(self, observe_agent):
        """
        Set whether the agent should be observable by a JsonObserver.
        :param observe_agent: Indicator of whether the agent should be observable through a JsonObserver.
        :return: self
        """
        self.observe_agent = observe_agent
        return self

    def with_export_qtable(self, export_qtable):
        """
        Set whether the Q-table should be exported upon finishing the training process.
        :param export_qtable: Indicator of whether the Q-table should be exported upon finishing the training process.
        :return: self
        """
        self.export_qtable = export_qtable
        return self

    def with_arlgorithm(self, arlgorithm: Type[AbstractQlearningARLgorithm]):
        """
        Set the arlgorithm to be used for training the agent.
        :param arlgorithm: The arlgorithm to be used for training the agent.
        :return: self
        """
        self.arlgorithm = arlgorithm
        return self

    def with_nb_episodes(self, nb_episodes):
        """
        Set the number of episodes.
        :param nb_episodes: The number of episodes
        :return: self
        """
        self.nb_episodes = nb_episodes
        return self

    def with_nb_of_eps_before_table_update(self, nb_of_eps_before_table_update):
        """
        Set the number of episodes before the Q-table should be updated by its shadow copy.
        :param nb_episodes: The number of episodes before the Q-table should be updated by its shadow copy.
        :return: self
        """
        self.nb_of_eps_before_table_update = nb_of_eps_before_table_update
        return self

    def with_qtable_convergence_threshold(self, qtable_convergence_threshold):
        """
        Set the threshold below which the Q-table should be considered converged.
        :param nb_episodes: The threshold below which the Q-table should be considered converged.
        :return: self
        """
        self.qtable_convergence_threshold = qtable_convergence_threshold
        return self

    def with_nb_steps_before_timeout(self, nb_steps_before_timeout):
        """
        Set the number of steps before an episode is terminated.
        :param nb_episodes: The number of steps before an episode is terminated.
        :return: self
        """

        self.nb_steps_before_timeout = nb_steps_before_timeout
        return self

    def with_random_rate(self, random_rate):
        """
        Set the epsilon for epsilon-greedy action selection.
        :param nb_episodes: The epsilon for epsilon-greedy action selection.
        :return: self
        """

        self.random_rate = random_rate
        return self

    def with_learning_rate(self, learning_rate):
        """
        Set the learning rate (alpha)
        :param nb_episodes: The learning rate
        :return: self
        """
        self.learning_rate = learning_rate
        return self

    def with_discount_factor(self, discount_factor):
        """
        Set the discount factor (gamma)
        :param nb_episodes: The discount factor
        :return: self
        """
        self.discount_factor = discount_factor
        return self

    def with_agent(self, agent: Agent):
        """
        Set the agent
        :param nb_episodes: The agent
        :return: self
        """
        self.agent = agent
        return self

    def _verify_hyperparameters(self):
        """
        Verify if enough information is provided to the trainer to train the agent. Raises an exception when this is not the case.
        :return: None
        """
        if self.arlgorithm is None:
            raise ValueError("Please specify a ARLgorithm to train with..")
        var_dict = self.__dict__
        if self.arlgorithm.__name__ == BellmanARLgorithm.__name__:
            var_dict = {key: var_dict[key] for key in {"discount_factor", "nb_episodes", "agent"}}
        none_keys = {key for key in var_dict if var_dict[key] is None}

        if len(none_keys) != 0:
            raise ValueError("Please first assign a value to the following parameters of the trainer: %s." % ", ".join(none_keys))

