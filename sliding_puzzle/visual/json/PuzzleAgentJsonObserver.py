from boarld.visual.json.JsonObserver import JsonObserver
import json

from sliding_puzzle.rl.agent.PuzzleAgent import PuzzleAgent


class PuzzleAgentJsonObserver(JsonObserver):
    def observable_to_json(self, observable):
        if not isinstance(observable, PuzzleAgent):
            raise ValueError(
                "Observable of type %s cannot be observed by an instance of PuzzleAgentJsonObserver." % observable.__class__.__name__)

        dic = {
            "nb_rows": observable.board.nb_rows,
            "nb_cols": observable.board.nb_cols,
            "state": observable.current_state.to_string()
        }

        return json.dumps(dic)