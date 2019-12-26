from boarld.core.rl.arlgorithm.QlearningARLgorithm import QlearningARLgorithm
from boarld.core.rl.runner.Runner import Runner
from boarld.core.rl.trainer.Trainer import Trainer
from boarld.gridworld.env.predefined.predefined_grids import *
from boarld.gridworld.rl.agent.GridAgent import GridAgent


# -- AGENT SETUP -- #
from boarld.core.rl.arlgorithm.DynaQARLgorithm import DynaQARLgorithm

from boarld.core.rl.arlgorithm.BellmanARLgorithm import BellmanARLgorithm

agent = GridAgent(Grid7.GRID)

# -- TRAINER SETUP -- #
trainer = Trainer() \
    .with_agent(agent) \
    .with_arlgorithm(BellmanARLgorithm) \
    .with_nb_episodes(3000) \
    .with_nb_of_eps_before_table_update(50) \
    .with_qtable_convergence_threshold(.001) \
    .with_nb_steps_before_timeout(1000) \
    .with_random_rate(0.3) \
    .with_learning_rate(0.2) \
    .with_discount_factor(0.7) \
    .with_export_qtable(True) \
    # .with_observe_agent(True) \
    # .with_observe_qtable(True) \

trainer.train()

# -- RUN -- #
runner = Runner() \
    .with_agent(agent) \
    # .with_qtable_imported_from('...')

runner.run()