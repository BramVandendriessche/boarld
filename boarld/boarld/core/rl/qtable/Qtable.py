import json
import pickle
from math import inf, isinf
from random import randint
from typing import Set, List

from boarld.core.env.action.Action import Action
from boarld.core.env.state.State import State
from boarld.core.util.observ.JsonObservable import JsonObservable


class Qtable(JsonObservable):
    """
    Representation of a Q-table, indicating the quality of an action in a certain state.
    The class contains a snapshot for measuring convergence and a shadow copy which can be used to update Q-values,
    but making choices based on the old table.
    """

    def __init__(self, possible_actions: Set[Action], default_value=0):
        """
        Construct a Q-table.
        :param possible_actions: Set of all possible actions.
        :param default_value: Default value for each (state, action)
        """
        super().__init__()
        self.possible_states: Set[State] = set()
        self.possible_actions: Set[Action] = possible_actions
        self.default_value = default_value
        self.table = {}
        self.shadowTable = {}
        self.snapshot = self.shadowTable.copy()

    def serialize(self):
        stateset = set([st for st, _ in self.table.keys()])
        res = [{**{ac.to_string().lower(): str(self.table[(st, ac.to_string())]) for ac in
                   self.possible_actions}, **{"state": st}} for st in stateset]
        return json.dumps(res)

    def get_Q_value(self, state: State, action: Action, replace_neg_inf_by_default_value: bool = False):
        """
        Get the q-value of the given state and action. Values are looked up in the table, not in its shadow copy
        containing the most recent values.
        :param state: The given state
        :param action: The given action; could be None.
        :param replace_neg_inf_by_default_value: Should -inf values be replaced by the default value? False by default.
        :return: Q(state, action). If action is None, the default value is returned. If the table did not yet contain
        a value for (state, action), the default value is returned. If replace_neg_inf_by_default_value is True and
        Q(state, action) is -inf, the default value is returned.
        """
        if state not in self.possible_states:
            self.add_state_and_actions_to_table(state)
        if action is None:
            return self.default_value

        key = (state.to_string(), action.to_string())
        if key not in self.table or (isinf(self.table[key]) and self.table[key] < 0):
            if replace_neg_inf_by_default_value:
                return self.default_value
            return -inf
        return self.table[key]

    def update_value(self, state: State, action: Action, value):
        """
        Update Q(state, action) to the given value. Note that this action does not take effect until
        update_table_by_shadow() is called.
        :param state: The given state
        :param action: The given action
        :param value: The new value of Q(state, action)
        :return: None
        """
        key = (state.to_string(), action.to_string())
        if state not in self.possible_states:
            self.add_state_and_actions_to_table(state)
        self.shadowTable[key] = value

    def add_state_and_actions_to_table(self, state):
        """
        Add Q(state, action) to the Q-table with value -inf for each possible action.
        :param state: The given state
        :return: None
        """
        self.possible_states.add(state)
        for ac in self.possible_actions:
            key = state.to_string(), ac.to_string()
            if key not in self.shadowTable:
                self.shadowTable[state.to_string(), ac.to_string()] = -inf

    def update_table_by_shadow(self):
        """
        Update the Q-table with the shadow copy.
        :return: None
        """
        self.table = dict(self.shadowTable)
        self.notify_observers_of_change()

    def get_list_of_greedy_best_actions(self, state: State, possible_actions: List[Action] = None):
        """
        Get a list of the best actions in the given state.
        :param state: The state in which the highest-quality actions should be considered.
        :param possible_actions: List of actions to be considered in the given state. If None, all possible actions
        are considered.
        :return: A list of actions yielding the highest Q-value.
        """
        if possible_actions is None:
            actions = self.possible_actions
        else:
            actions = possible_actions
        actions_and_rewards = [(ac, self.get_Q_value(state, ac)) for ac in actions]
        if len(actions_and_rewards) == 0:
            return []
        _, val = sorted(actions_and_rewards, key=lambda x: x[1], reverse=True)[0]

        return [(a, v) for a, v in actions_and_rewards if val == v]

    def get_greedy_best_action(self, state: State, possible_actions: List[Action] = None):
        """
        Get the action yielding the highest Q-value in the given state.
        :param state: The state for which the best action should be found.
        :param possible_actions: List of actions to be considered in the given state. If None, all possible actions
        are considered.
        :return: The action yielding the highest Q-value in the given state. If multiple actions are equally valuable,
        one of these is returned randomly.
        """
        greedy_best_actions = self.get_list_of_greedy_best_actions(state, possible_actions)
        if len(greedy_best_actions) == 0:
            return None, None
        ac, val = greedy_best_actions[0]
        if len(greedy_best_actions) > 1:
            ac, val = greedy_best_actions[randint(0, len(greedy_best_actions) - 1)]
        return ac, val

    def take_snapshot(self):
        """
        Take a snapshot of the Q-table in its current state. Note that the snapshot is taken from the shadow copy.
        :return: None
        """
        self.snapshot = self.shadowTable.copy()

    def has_converged_since_last_snapshot(self, threshold):
        """
        Calculate if the Q-table has converged, based on the most recent snapshot and the given threshold.
        :param threshold: The threshold below which max({abs(Qvalue(state, action) - snapshot(state, action) for each (state, action)})
        should be for the Q-table to be considered converged.
        :return: True if max({abs(Qvalue(state, action) - snapshot(state, action) for each (state, action)}) < threshold,
        else False.
        """
        if self.shadowTable.keys() != self.snapshot.keys():
            return False
        else:
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
        """
        Export the Q-table to a .p (pickle) file with the given filename.
        :param filename: Filename of the exported Q-table.
        :return: None
        """
        with open(filename, 'wb') as file:
            state = self.__dict__.copy()
            del state['observers']
            pickle.dump(state, file)

    @staticmethod
    def from_file(filename):
        """
        Load a Q-table from a .p (pickle) file with the given filename.
        :param filename: Filename of the .p file.
        :return: Loaded Q-table.
        """
        with open(filename, 'rb') as file:
            table = Qtable(set())
            table.__dict__.update(pickle.load(file))
            return table
