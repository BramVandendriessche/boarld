import json

from boarld.visual.json.JsonObserver import JsonObserver
from gridworld.rl.agent.GridAgent import GridAgent


class GridAgentJsonObserver(JsonObserver):
    def observable_to_json(self, observable):
        if not isinstance(observable, GridAgent):
            raise ValueError(
                "Observable of type %s cannot be observed by an instance of GridAgentObserver." % observable.__class__.__name__)

        # TODO: +1 ok?
        dic = {
            "board_setup": {
                "nb_rows": observable.board.nb_rows,
                "nb_cols": observable.board.nb_cols,
                "holes": [[x + 1, y + 1] for x, y in observable.board.snake_pits.keys()],
                "obstacles": [[x + 1, y + 1] for x, y in observable.board.walls.keys()],
                "footsteps": [[st.data.x + 1, st.data.y + 1] for st in observable.traveled_path],
                "start": [observable.init_state.data.x + 1, observable.init_state.data.y + 1],
                "end": [[x + 1, y + 1] for x,y in observable.board.goals]
            },
            "best_path_now": [[st.data.x, st.data.y] for st in
                              observable.get_greedy_best_path_from_state_to_goal(observable.init_state)[1]],
            "best_actions": [
                {"x": cell.x + 1, "y": cell.y + 1,
                 "actions": [ac.to_string() for ac,_ in observable.Qtable.get_list_of_greedy_best_actions(observable.map_cell_to_state(cell))]}
                for cell in observable.board.cell_set
            ]

        }
        # print(dic)
        return json.dumps(dic)
