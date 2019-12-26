from boarld.core.rl.arlgorithm.QlearningARLgorithm import QlearningARLgorithm
from boarld.core.rl.trainer.Trainer import Trainer
from boarld.core.rl.runner.Runner import Runner
from boarld.sliding_puzzle.env.board.SlidingPuzzle import SlidingPuzzle
from boarld.sliding_puzzle.rl.agent.PuzzleAgent import PuzzleAgent

# -- BOARD SETUP -- #
nb_rows = 2
nb_cols = 2
puzz = SlidingPuzzle(nb_rows, nb_cols)

# -- AGENT SETUP -- #
agent = PuzzleAgent(puzz)

# -- TRAINER SETUP -- #
trainer = Trainer() \
    .with_agent(agent) \
    .with_arlgorithm(QlearningARLgorithm) \
    .with_nb_episodes(1000) \
    .with_nb_of_eps_before_table_update(50) \
    .with_qtable_convergence_threshold(.001) \
    .with_nb_steps_before_timeout(1000) \
    .with_random_rate(0.3) \
    .with_learning_rate(0.2) \
    .with_discount_factor(0.7) \
    .with_export_qtable(True) \
    # .with_observe_agent(True) \
    # .with_observe_qtable(True) \

# -- TRAIN -- #
trainer.train()

# -- RUN -- #
runner = Runner() \
    .with_agent(agent) \
    # .with_qtable_imported_from('SlidingPuzzle_2x2_QlearningARLgorithm_1000_episodes')
agent.set_agent_to_random_state(nb_actions=100)

runner.run()