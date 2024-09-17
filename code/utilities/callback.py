from stable_baselines3.common.callbacks import BaseCallback
import csv
import pandas as pd
import time

class SaveModelAndMetricsCallback(BaseCallback):
    """
    Used by the RL algorithm to save custom metrics and the model during training
    Must be included in the learn() method of the algorithm
    """
    def __init__(self, model_path, metrics_path, episodes_path, existing=False, verbose=1):
        super(SaveModelAndMetricsCallback, self).__init__(verbose)

        # metric trackers
        self.best_reward = -1000
        self.n_updates = 0
        self.n_episodes = 0
        self.total_n_episodes = 0
        self.episode_start_time = time.time()

        # file paths
        self.model_path = model_path
        self.metrics_path = metrics_path
        self.episodes_path = episodes_path

        if not existing: # if the model doesn't already exist
            # Initialize the CSV file for metrics
            with open(self.metrics_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Episode', 'Time'])
            
            # Initialize the CSV file for number of episodes
            with open(self.episodes_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Update', 'Episodes', 'Total Episodes'])
        else:
            # Load the previous metrics to use for further tracking
            df = pd.read_csv(self.metrics_path)
            self.best_reward = 0 # this can be changed to the best reward of the model before loading
            self.n_episodes = df.iloc[-1, 0]

            df = pd.read_csv(self.episodes_path)
            self.n_updates = df.iloc[-1, 0]
            self.total_n_episodes = df.iloc[-1, 2]

    def _on_step(self):
        """
        Is called every timestep to check if the episode has ended
        Uses the locals attribute to confirm termination
        This implementation only saves the time taken for the episode to a csv
        """

        if self.locals.get('done', False):
            t = time.time() - self.episode_start_time
            self.episode_start_time = time.time()

            # Save metrics to CSV
            with open(self.metrics_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([self.n_episodes, t])

            self.n_episodes += 1

        return True # return True to continue training
    
    def _on_rollout_end(self):
        """
        Is called at the end of a policy update
        Saves the model and the number of episodes for the policy update
        """

        mean_reward = self.logger.name_to_value['rollout/ep_rew_mean'] # take the episode mean reward from the logger
        if mean_reward > self.best_reward: # if better than any previous mean rewards
            self.model.save(self.model_path) # save the "best" model
            self.best_reward = mean_reward

        self.model.save(self.model_path + "_final") # save the model again separately for comparison to best

        # compute the episode metrics
        n_recent_epsiodes = self.n_episodes - self.total_n_episodes
        self.total_n_episodes = self.n_episodes
        self.n_updates += 1
        
        # save the metrics
        with open(self.episodes_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.n_updates, n_recent_epsiodes, self.total_n_episodes]) 