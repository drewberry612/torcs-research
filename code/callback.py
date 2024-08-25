from stable_baselines3.common.callbacks import BaseCallback
import csv
import pandas as pd
import time

class SaveModelAndMetricsCallback(BaseCallback):
    def __init__(self, model_path, metrics_path, episodes_path, existing=False, verbose=1):
        super(SaveModelAndMetricsCallback, self).__init__(verbose)
        self.best_reward = -1000
        self.n_updates = 0
        self.n_episodes = 0
        self.total_n_episodes = 0
        self.model_path = model_path
        self.metrics_path = metrics_path
        self.episodes_path = episodes_path
        self.episode_start_time = time.time()

        if not existing:
            # Initialize the CSV file for metrics
            with open(self.metrics_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Episode', 'Time'])

            with open(self.episodes_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Update', 'Episodes', 'Total Episodes'])
        else:
            df = pd.read_csv(self.metrics_path)
            self.best_reward = 0 # sort this out, not really a big priority just take it from the previous logger
            self.n_episodes = df.iloc[-1, 0]

            df = pd.read_csv(self.episodes_path)
            self.n_updates = df.iloc[-1, 0]
            self.total_n_episodes = df.iloc[-1, 2]

    def _on_step(self):
        if self.locals.get('done', False):
            t = time.time() - self.episode_start_time
            self.episode_start_time = time.time()

            # Save metrics to CSV
            with open(self.metrics_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([self.n_episodes, t])

            self.n_episodes += 1

        return True
    
    def _on_rollout_end(self):
        mean_reward = self.logger.name_to_value['rollout/ep_rew_mean']
        if mean_reward > self.best_reward:
            self.model.save(self.model_path)
            self.best_reward = mean_reward

        self.model.save(self.model_path + "_final")

        n_recent_epsiodes = self.n_episodes - self.total_n_episodes
        self.total_n_episodes = self.n_episodes
        self.n_updates += 1
        
        with open(self.episodes_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.n_updates, n_recent_epsiodes, self.total_n_episodes]) 