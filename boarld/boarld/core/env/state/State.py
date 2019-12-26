class State:
    """
    Class representing a state. The state contains data of any type, offering more information about the state.
    """
    def __init__(self, data: any):
        """
        Construct a state containing the given data.
        :param data: Data of any type, containing more information about the state.
        """
        self.data: any = data

    def to_string(self):
        """
        Get a textual representation of the state.
        :return: A textual representation of the state.
        """
        return self.data.to_string()