from paho.mqtt.client import Client

from sliding_puzzle.env.board.SlidingPuzzle import SlidingPuzzle
from sliding_puzzle.rl.agent.PuzzleAgent import PuzzleAgent
from boarld.rl.brain.QlearningBrain import QlearningBrain
from boarld.rl.brain.SarsaBrain import SarsaBrain
from boarld.visual.json.QtableJsonObserver import QtableJsonObserver
from sliding_puzzle.visual.json.PuzzleAgentJsonObserver import PuzzleAgentJsonObserver

################################################
            #### CONFIGURE THIS ####
################################################
# -- VISUALISATION -- #
withQtableJson = True
withAgentJson = True
export_qtable = True

# -- BOARD SETUP -- #
nb_rows = 2
nb_cols = 2

# -- TRAINING SETUP -- #
brain = QlearningBrain
nb_episodes = 100000
nb_of_eps_before_table_update=50
qtable_convergence_threshold=.001
nb_steps_before_timeout=1000
random_rate=0.3
learning_rate=0.2
discount_factor=0.7

# -- AGENT SETUP -- #
step_reward=-1
goal_reward=1

########################################################################
########################################################################
########################################################################

args = (brain, nb_episodes, nb_of_eps_before_table_update, qtable_convergence_threshold, nb_steps_before_timeout,
        random_rate, learning_rate, discount_factor)
puzz = SlidingPuzzle(nb_rows, nb_cols)
agent = PuzzleAgent(puzz, step_reward, goal_reward)

if withQtableJson or withAgentJson:
    client = Client('main', transport='websockets')
    client.connect('localhost', 9001)
    if withQtableJson:
        qtable_obs = QtableJsonObserver(client)
        qtable_obs.add_observable(agent.Qtable)
    if withAgentJson:
        agent_obs = PuzzleAgentJsonObserver(client)
        agent_obs.add_observable(agent)

agent.learn(*args)
print('Number of states in Q-table: %s' % len(agent.Qtable.possible_states))
agent.Qtable.showQtable()

agent.Qtable.to_file('puzzle_%sx%s_qtable_%s_episodes.p' % (nb_rows, nb_cols, nb_episodes))
