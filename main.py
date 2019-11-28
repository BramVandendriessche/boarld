import threading

from boarld.rl.qtable.Qtable import Qtable
from paho.mqtt.client import Client

from boarld.rl.brain.QlearningBrain import QlearningBrain
from boarld.rl.brain.SarsaBrain import SarsaBrain
from boarld.visual.json.QtableJsonObserver import QtableJsonObserver
from gridworld.env.predef_envs import predef_envs
from gridworld.rl.agent.GridAgent import GridAgent
from gridworld.visual.json.GridAgentJsonObserver import GridAgentJsonObserver
from gridworld.visual.tk.VisualGridAgentTraining import VisualGridAgentTraining

################################################
            #### CONFIGURE THIS ####
################################################

# -- VISUALISATION -- #
withVisual = False
withQtableJson = False
withAgentJson = True
export_qtable = False

# -- BOARD SETUP -- #
env =  predef_envs.Env7
# -- TRAINING SETUP -- #
brain = QlearningBrain  # or SarsaBrain
nb_episodes = 100000
nb_of_eps_before_table_update = 50
qtable_convergence_threshold = .001
nb_steps_before_timeout = 1000
random_rate = 0.3
learning_rate = 0.2
discount_factor = 0.7
vg_type = VisualGridAgentTraining  # or VisualBestPath

# -- AGENT SETUP -- #
step_reward = -1
goal_reward = 10
snakepit_reward = -10

########################################################################
########################################################################
########################################################################

args = (brain, nb_episodes, nb_of_eps_before_table_update, qtable_convergence_threshold, nb_steps_before_timeout,
        random_rate, learning_rate, discount_factor)
agent = GridAgent(env.GRID, step_reward, goal_reward, snakepit_reward)
agent.Qtable = Qtable.from_file('gridworld_Env7_6x6_100000_episodes.p')
if withQtableJson or withAgentJson:
    client = Client('main', transport='websockets')
    client.connect('localhost', 9001)
    if withQtableJson:
        qtable_obs = QtableJsonObserver(client)
        qtable_obs.add_observable(agent.Qtable)
    if withAgentJson:
        agent_obs = GridAgentJsonObserver(client)
        agent_obs.add_observable(agent)

if withVisual:
    vg = vg_type(agent)
    thr = threading.Thread(target=agent.learn, args=args)
    thr.start()
    vg.mainloop()
else:
    agent.learn(*args)
    agent.Qtable.showQtable()
if export_qtable:
    agent.Qtable.to_file('gridworld_%s_%sx%s_%s_episodes.p' %(env.__name__, env.GRID.nb_rows, env.GRID.nb_cols, nb_episodes))
