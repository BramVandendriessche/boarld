import time

from boarld.rl.qtable.Qtable import Qtable
from boarld.util.observ.JsonObservable import JsonObservable
from boarld.util.observ.Observable import Observable
from boarld.util.observ.Observer import Observer
from boarld.visual.json import Topics
from gridworld.rl.agent.GridAgent import GridAgent
from paho.mqtt.client import Client
from sliding_puzzle.rl.agent.PuzzleAgent import PuzzleAgent


class JsonObserver(Observer):

    def __init__(self, client: Client):
        super().__init__()
        self.client: Client = client

    def act_on_notify(self, observable: JsonObservable):
        # TODO: to reconnect or not to reconnect, that's the question..
        if not isinstance(observable, JsonObservable):
            raise ValueError("Observable %s is not of type JsonObservable." % observable)
        time.sleep(.3)
        # self.client.reconnect()
        self.client.publish(self.map_topic(observable), observable.serialize())

    @staticmethod
    def map_topic(observable: Observable):
        if isinstance(observable, Qtable):
            return Topics.QTABLE
        elif isinstance(observable, GridAgent):
            return Topics.STATE_GRIDWORLD
        elif isinstance(observable, PuzzleAgent):
            return Topics.STATE_SLIDING_PUZZLE
        else:
            raise ValueError("Observable of type %s does not have a specified topic." % observable.__class__.__name__)
