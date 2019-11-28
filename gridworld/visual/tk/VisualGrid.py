from gridworld.visual.tk import AbstractVisualGrid
from boarld.util.observ.Observable import Observable


class VisualGrid(AbstractVisualGrid):
    def act_on_notify(self, observable: Observable):
        pass