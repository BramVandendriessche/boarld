from abc import abstractmethod
import progressbar

from boarld.core.rl.arlgorithm.ARLgorithm import ARLgorithm


class AbstractQlearningARLgorithm(ARLgorithm):
    """
    Extension of ARLgorithm of which learn() follows a specific template:
        ```
        during n episodes:
            if the Q-table has converged or a certain number of episodes have passed:
                update the Q-table by its shadow
            else:
                take a new snapshot of the Q-table
            set the agent to a random state
            run an episode
        ```
    An implementation of the episode is defined by children of AbstractQlearningARLgorithm.
    """

    @abstractmethod
    def episode(self, nb_steps_before_timeout, random_rate, learning_rate, discount_factor):
        """
        Defines one episode of the training process.
        :param nb_steps_before_timeout: The number of steps the agent is allowed to perform before the episode is terminated.
        :param random_rate: Epsilon for epsilon-greedy action selection: the best action is selected with a probability of
        (1-random_rate), a random action is selected with a random_rate probability.
        :param learning_rate: The learning rate (alpha) determines to what extent newly acquired information should
        be incorporated in the agent's knowledge. A learning rate of 0 yields in zero learning, a value of 1 makes the
        agent only use the newest information.
        :param discount_factor: The discount factor (gamma) determines the importance of future rewards: A discount
        factor of 0 makes the agent only consider current rewards, a value close to 1 makes it aim for long-term rewards.
        :return: None
        """
        pass

    def learn(self, nb_episodes, nb_of_eps_before_table_update, qtable_convergence_threshold,
              nb_steps_before_timeout, random_rate=0.3, learning_rate=0.2, discount_factor=0.7):
        table_counter = 0
        for i in progressbar.progressbar(range(nb_episodes)):
            if table_counter >= nb_of_eps_before_table_update or self.agent.Qtable.has_converged_since_last_snapshot(qtable_convergence_threshold):
                self.agent.Qtable.update_table_by_shadow()
                table_counter = 0
            else:
                self.agent.Qtable.take_snapshot()
            table_counter += 1
            self.agent.set_agent_to_random_state(nb_actions=min(max(int(i / 10), 1), 101))
            self.episode(nb_steps_before_timeout, random_rate, learning_rate, discount_factor)
        print('Done learning!')
