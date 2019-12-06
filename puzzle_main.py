from boarld.rl.brain.QlearningBrain import QlearningBrain
from boarld.trainers_and_runners.Trainer import Trainer
from boarld.trainers_and_runners.Runner import Runner
from sliding_puzzle.env.board.SlidingPuzzle import SlidingPuzzle
from sliding_puzzle.rl.agent.PuzzleAgent import PuzzleAgent

# -- BOARD SETUP -- #
nb_rows = 2
nb_cols = 2
puzz = SlidingPuzzle(nb_rows, nb_cols)

# -- AGENT SETUP -- #
agent = PuzzleAgent(puzz)

# -- TRAINER SETUP -- #
trainer = Trainer() \
    .with_agent(agent) \
    .with_brain(QlearningBrain) \
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
    # .with_qtable_imported_from('SlidingPuzzle_2x2_QlearningBrain_1000_episodes')
agent.set_agent_to_random_state(nb_actions=100)

runner.run()