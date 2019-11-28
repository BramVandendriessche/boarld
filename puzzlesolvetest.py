import threading

from boarld.rl.qtable.Qtable import Qtable
from sliding_puzzle.env.board.SlidingPuzzle import SlidingPuzzle
from sliding_puzzle.visual.tk.PuzzleGraphics import PuzzleGraphics
from sliding_puzzle.rl.agent.PuzzleAgent import PuzzleAgent


nb_rows = 2
nb_cols = 2
nb_episodes = 1000

table = Qtable.from_file('puzzle_%sx%s_qtable_%s_episodes.p' % (nb_rows, nb_cols, nb_episodes))

puzz = SlidingPuzzle(nb_rows, nb_cols)
agent = PuzzleAgent(puzz)
agent.shuffle_n_actions(100)

agent.Qtable = table
agent.possible_states = agent.Qtable.possible_states

thr = threading.Thread(target=agent.solve)
pg = PuzzleGraphics(puzz)
thr.start()

pg.mainloop()
