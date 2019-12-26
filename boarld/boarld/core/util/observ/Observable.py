

class Observable:
    """
    Abstract implementation of the Observable in an Observer pattern. An observer subscribes to notifications of an
    Observable. The latter notifies the former when it has undergone relevant changes.
    """
    def __init__(self):
        """
        Construct an Observable.
        """
        self.observers = set()

    def add_observer(self, observer):
        """
        Add an observer to the Observable's list of observers.
        :param observer: The Observer subscribing to notification of the Observable.
        :return: None
        """
        self.observers.add(observer)

    def remove_observer(self, observer):
        """
        Remove an observer from the observable's list of observers.
        :param observer: The observer unsubscribing from notification of the observable.
        :return: None
        """
        self.observers.remove(observer)

    def notify_observers_of_change(self):
        """
        Notify subscribed observers of a change in the observable.
        :return: None
        """
        for observer in self.observers:
            observer.notify(self)
