class Action:
    """
    A class representing an Action.
    """

    def to_string(self):
        return self.__class__.__name__


class Up(Action):
    """
    A class representing the "up" action.
    """
    pass



class Down(Action):
    """
    A class representing the "down" action.
    """
    pass


class Left(Action):
    """
    A class representing the "left" action.
    """
    pass


class Right(Action):
    """
    A class representing the "right" action.
    """
    pass
