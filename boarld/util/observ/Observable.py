

class Observable:
    def __init__(self):
        self.observers = set()

    def add_observer(self, observer):
        self.observers.add(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers_of_change(self):
        for observer in self.observers:
            observer.notify(self)
