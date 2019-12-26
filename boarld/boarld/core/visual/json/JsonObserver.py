import time

from boarld.core.rl.qtable.Qtable import Qtable
from boarld.core.util.observ.JsonObservable import JsonObservable
from boarld.core.util.observ.Observable import Observable
from boarld.core.util.observ.Observer import Observer
from boarld.core.visual.json import Topics
from boarld.gridworld.rl.agent.GridAgent import GridAgent
from paho.mqtt.client import Client
from boarld.sliding_puzzle.rl.agent.PuzzleAgent import PuzzleAgent


class JsonObserver(Observer):
    """
    The goal of a JsonObserver is to subscribe to JsonObservables and publish their new states on an MQTT queue.
    """

    def __init__(self, client: Client):
        """
        Construct a JsonObserver with a given MQTT client
        :param client: The MQTT client (paho.mqtt.client.Client).
        """
        super().__init__()
        self.client: Client = client

    def act_on_notify(self, observable: JsonObservable):
        if not isinstance(observable, JsonObservable):
            raise ValueError("Observable %s is not of type JsonObservable." % observable)
        time.sleep(.3)
        self.client.publish(self.map_topic(observable), observable.serialize())

    @staticmethod
    def map_topic(observable: Observable) -> str:
        """
        Return an MQTT topic based on the type observable. Currently, supported types are: Qtable, GridAgent, PuzzleAgent.
        :param observable: The observable for which the topic should be determined.
        :return: The MQTT topic
        """
        if isinstance(observable, Qtable):
            return Topics.QTABLE
        elif isinstance(observable, GridAgent):
            return Topics.STATE_GRIDWORLD
        elif isinstance(observable, PuzzleAgent):
            return Topics.STATE_SLIDING_PUZZLE
        else:
            raise ValueError("Observable of type %s does not have a specified topic." % observable.__class__.__name__)
