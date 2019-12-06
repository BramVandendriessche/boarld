from paho.mqtt.client import Client

from boarld.rl.agent.Agent import Agent
from boarld.rl.brain.Brain import Brain
from boarld.visual.json.JsonObserver import JsonObserver
from boarld.util.mqtt_params import mqtt_params


class Trainer:

    def __init__(self):
        self.observe_qtable = False
        self.observe_agent = False
        self.export_qtable = False
        self.brain = None
        self.nb_episodes = 0
        self.nb_of_eps_before_table_update = 0
        self.qtable_convergence_threshold = 0
        self.nb_steps_before_timeout = 0
        self.random_rate = 0
        self.learning_rate = 0
        self.discount_factor = 0
        self.agent = None

    def train(self):
        if self.observe_agent or self.observe_qtable:
            client = Client('main', transport='websockets')
            client.connect(mqtt_params.MQTT_HOST, mqtt_params.MQTT_PORT)
            observer = JsonObserver(client)

            if self.observe_qtable:
                observer.add_observable(self.agent.Qtable)
            if self.observe_agent:
                observer.add_observable(self.agent)
        args = \
            (self.brain, self.nb_episodes, self.nb_of_eps_before_table_update, self.qtable_convergence_threshold,
             self.nb_steps_before_timeout, self.random_rate, self.learning_rate, self.discount_factor)
        self.agent.learn(*args)

        if self.export_qtable:
            self.agent.Qtable.to_file(
                '%s_%s_%s_episodes.p' % (self.agent.board.name, self.brain.__name__, self.nb_episodes))

    def with_observe_qtable(self, observe_qtable):
        self.observe_qtable = observe_qtable
        return self

    def with_observe_agent(self, observe_agent):
        self.observe_agent = observe_agent
        return self

    def with_export_qtable(self, export_qtable):
        self.export_qtable = export_qtable
        return self

    def with_brain(self, brain: Brain):
        self.brain = brain
        return self

    def with_nb_episodes(self, nb_episodes):
        self.nb_episodes = nb_episodes
        return self

    def with_nb_of_eps_before_table_update(self, nb_of_eps_before_table_update):
        self.nb_of_eps_before_table_update = nb_of_eps_before_table_update
        return self

    def with_qtable_convergence_threshold(self, qtable_convergence_threshold):
        self.qtable_convergence_threshold = qtable_convergence_threshold
        return self

    def with_nb_steps_before_timeout(self, nb_steps_before_timeout):
        self.nb_steps_before_timeout = nb_steps_before_timeout
        return self

    def with_random_rate(self, random_rate):
        self.random_rate = random_rate
        return self

    def with_learning_rate(self, learning_rate):
        self.learning_rate = learning_rate
        return self

    def with_discount_factor(self, discount_factor):
        self.discount_factor = discount_factor
        return self

    def with_agent(self, agent: Agent):
        self.agent = agent
        return self
