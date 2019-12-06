import time

from paho.mqtt.client import Client

from boarld.rl.agent.Agent import Agent
from boarld.rl.qtable.Qtable import Qtable
from boarld.util.mqtt_params import mqtt_params
from boarld.visual.json.JsonObserver import JsonObserver


class Runner:

    def __init__(self):
        self.qtable_file_path = ''
        self.agent = None

    def run(self):
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
        self.agent = agent
        return self

    def with_qtable_imported_from(self, qtable_file_path):
        self.qtable_file_path = qtable_file_path
        return self
