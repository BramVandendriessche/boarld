import time
from paho.mqtt.client import Client

from boarld.core.rl.agent.Agent import Agent
from boarld.core.rl.qtable.Qtable import Qtable
from boarld.core.util.mqtt_params import mqtt_params
from boarld.core.visual.json.JsonObserver import JsonObserver


class Runner:
    """
    Runner to make a trained agent solve the problem it's been trained for.
    """

    def __init__(self):
        """
        Construct a runner.
        """
        self.qtable_file_path = ''
        self.agent = None

    def run(self):
        """
        Make the Runner's agent solve the problem it's been trained for. The agent should be defined using with_agent().
        If q_table_file_path is not set, the agent's current Q-table is used.
        :return: None
        """
        if self.agent is None:
            raise ValueError("Please assign an agent to the runner before running it.")

        client = Client('main', transport='websockets')
        client.connect(mqtt_params.MQTT_HOST, mqtt_params.MQTT_PORT)
        observer = JsonObserver(client)
        observer.add_observable(self.agent)

        if self.qtable_file_path:
            self.agent.Qtable = Qtable.from_file(self.qtable_file_path)
            observer.add_observable(self.agent.Qtable)
            self.agent.Qtable.notify_observers_of_change()
        time.sleep(3)

        self.agent.solve()

    def with_agent(self, agent: Agent):
        """
        Set the Runner's agent.
        :param agent: The agent to be used by the Runner to solve a problem.
        :return: self
        """
        self.agent = agent
        return self

    def with_qtable_imported_from(self, qtable_file_path):
        """
        Set the path from which the Q-table is to be loaded. If not set, the agent's current Q-table is used.
        :param qtable_file_path: Path to the exported Q-table.
        :return: self
        """
        self.qtable_file_path = qtable_file_path
        return self
