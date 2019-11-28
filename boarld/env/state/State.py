class State:
    def __init__(self, data: any):
        self.data: any = data

    def to_string(self):
        return self.data.to_string()