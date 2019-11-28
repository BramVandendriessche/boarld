from boarld.rl.qtable.Qtable import Qtable
from boarld.visual.json.JsonObserver import JsonObserver
import json


class QtableJsonObserver(JsonObserver):

    def observable_to_json(self, observable) -> str:
        if not isinstance(observable, Qtable):
            raise ValueError(
                "Observable of type %s cannot be observed by an instance of QtableObserver." % observable.__class__.__name__)

        # TODO: replace eval?
        stateset = set([st for st, _ in observable.table.keys()])
        res = [{**{ac.to_string().lower(): str(observable.table[(st, ac.to_string())]) for ac in observable.possible_actions}, **{"state": st}} for st in stateset ]

        return json.dumps(res)
