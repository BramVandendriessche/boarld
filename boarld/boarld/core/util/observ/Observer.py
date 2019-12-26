from abc import ABC, abstractmethod

from boarld.core.util.observ.Observable import Observable


class Observer(ABC):
    """
    Abstract implementation of the Observer in an Observer pattern. An observer subscribes to notifications of an
    Observable. The latter notifies the former when it has undergone relevant changes.
    """
    def __init__(self):
        """Construct an Observer."""
        self.observables = set()

    def notify(self, observable: Observable):
        """
        Method to be called by an observable when it has undergone relevant changes.
        :param observable: The observable responsible for the notification.
        :return: None
        """
        if observable in self.observables:
            self.act_on_notify(observable)
        else:
            raise ValueError("Observer is not subscribed to observable.")

    @abstractmethod
    def act_on_notify(self, observable: Observable):
        """
        Action undertaken by the observer upon notification by the Observable.
        :param observable: The observable responsible for the notification.
        :return: None
        """
        pass

    def add_observable(self, observable: Observable):
        """
        Add observable to the "watchlist" of the Observer, i.e. subscribe the Observer to notifications of the given Observable.
        :param observable: Observable to which the Observer subscribes
        :return: None
        """
        if observable not in self.observables:
            self.observables.add(observable)
            observable.add_observer(self)

    def remove_observable(self, observable: Observable):
        """
        Remove observable from the Observer's "watchlist", i.e. unsubscribe the Observer from notifications of the given Observable.
        :param observable: Observable from which the Observer unsubscribes.
        :return: None
        """
        if observable in self.observables:
            self.observables.remove(observable)
            observable.remove_observer(self)
