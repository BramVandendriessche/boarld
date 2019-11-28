class Action:
    
    @staticmethod
    def to_string():
        return __class__.__name__


class Up(Action):
    @staticmethod
    def to_string():
        return __class__.__name__


class Down(Action):
    @staticmethod
    def to_string():
        return __class__.__name__


class Left(Action):
    @staticmethod
    def to_string():
        return __class__.__name__


class Right(Action):
    @staticmethod
    def to_string():
        return __class__.__name__

