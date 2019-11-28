from abc import ABC, abstractmethod

from boarld.util.observ.Observable import Observable


class Observer(ABC):
    def __init__(self):
        self.observables = set()

    def notify(self, observable: Observable):
        if observable in self.observables:
            self.act_on_notify(observable)
        else:
            raise ValueError("Observer is not subscribed to observable.")

    @abstractmethod
    def act_on_notify(self, observable: Observable):
        pass

    def add_observable(self, observable: Observable):
        if observable not in self.observables:
            self.observables.add(observable)
            observable.add_observer(self)

    def remove_observable(self, observable: Observable):
        if observable in self.observables:
            self.observables.remove(observable)
            observable.remove_observer(self)
