class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def has_same_position(self, co):
        return self.x == co.x and self.y == co.y

    def to_string(self):
        return str((self.x, self.y))
