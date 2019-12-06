from abc import abstractmethod

from boarld.util.observ.Observable import Observable


class JsonObservable(Observable):
    @abstractmethod
    def serialize(self): pass
