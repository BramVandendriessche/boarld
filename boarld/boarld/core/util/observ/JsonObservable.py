from abc import abstractmethod

from boarld.core.util.observ.Observable import Observable


class JsonObservable(Observable):
    """
    Observable with the capability of serializing its current state.
    """
    @abstractmethod
    def serialize(self) -> str:
        """
        Serialize the observable's state to a JSON-based representation.
        :return: JSON-based representation of the observable's state.
        """
        pass
