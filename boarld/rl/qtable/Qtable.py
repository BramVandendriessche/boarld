import pickle
from math import inf, isinf
from random import randint
from typing import Set, List

from boarld.env.action.Action import Action
from boarld.env.state.State import State
from boarld.util.observ.Observable import Observable


class Qtable(Observable):

    def __init__(self, possible_actions: Set[Action.__class__], default_value=0):
        super().__init__()
        self.possible_states: Set[State] = set()
        self.possible_actions: Set[Action.__class__] = possible_actions
        self.default_value = default_value
        self.table = {}
        self.shadowTable = {}
        self.snapshot = self.shadowTable.copy()

    def get_Q_value(self, state: State, action: Action, replace_neg_inf_by_default_value: bool = False):
        key = (state.to_string(), action.to_string())
        if state not in self.possible_states:
            self.add_state_and_actions_to_table(state)
        if key not in self.table or isinf(self.table[key]):
            if replace_neg_inf_by_default_value:
                return self.default_value
            return -inf
        return self.table[key]

    def update_value(self, state: State, action: Action, value):
        key = (state.to_string(), action.to_string())
        if state not in self.possible_states:
            self.add_state_and_actions_to_table(state)
        self.shadowTable[key] = value

    def add_state_and_actions_to_table(self, state):
        self.possible_states.add(state)
        for ac in self.possible_actions:
            key = state.to_string(), ac.to_string()
            if key not in self.shadowTable:
                self.shadowTable[state.to_string(), ac.to_string()] = -inf

    def update_table_by_shadow(self):
        self.table = dict(self.shadowTable)
        self.notify_observers_of_change()

    def get_list_of_greedy_best_actions(self, state: State, possible_actions: List[Action] = None):
        if possible_actions is None:
            actions = self.possible_actions
        else:
            actions = possible_actions
        actions_and_rewards = [(ac, self.get_Q_value(state, ac)) for ac in actions]
        ac, val = sorted(actions_and_rewards, key=lambda x: x[1], reverse=True)[0]

        # return random action if some actions yield equal Q-values
        actions_and_rewards = [(a, v) for a, v in actions_and_rewards if val == v]
        return actions_and_rewards

    def get_greedy_best_action(self, state: State, possible_actions: List[Action] = None):
        greedy_best_actions = self.get_list_of_greedy_best_actions(state, possible_actions)
        ac,val = greedy_best_actions[0]
        if len(greedy_best_actions) > 1:
            ac, val = greedy_best_actions[randint(0, len(greedy_best_actions) - 1)]
        return ac, val

    def take_snapshot(self):
        self.snapshot = self.shadowTable.copy()

    def has_converged_since_last_snapshot(self, threshold):
        if self.shadowTable.keys() != self.snapshot.keys():
            return False
        else:
            # denom = max({abs(v) + 1 for v in self.shadowTable.values()})
            diffs = {abs(self.shadowTable[key] - self.snapshot[key])
                     if self.shadowTable[key] != -inf or self.snapshot[key] != -inf
                     else 0 for key in self.shadowTable}
            return max(diffs) < threshold

    # TODO: formatting
    def showQtable(self):
        if len(self.possible_states) != 0:
            length = len(list(self.possible_states)[0].to_string())
        else:
            length = 10
        head = '|  Cell'.center(length)
        for act in self.possible_actions:
            head += '| ' + act.to_string().center(length)
        head += '| '
        print(head)
        print('-----------------------------------------------------------')
        for state in sorted(self.possible_states, key=lambda x: x.to_string()):
            out = ('| %s' % state.to_string()).center(length) + '| '
            for ac in self.possible_actions:
                val = round(self.get_Q_value(state, ac), 4)
                out += ('%.5f ' % val).center(length) + '| '
            print(out)

    def to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def from_file(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
