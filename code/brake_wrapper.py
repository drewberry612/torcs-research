import gymnasium as gym
import numpy as np
import random

class RandomBrakeWrapper(gym.Wrapper):
    def __init__(self, env):
        super(RandomBrakeWrapper, self).__init__(env)
        self.timestep = 0

    def step(self, action):
        self.timestep += 1
        modified_action = np.copy(action)
        if random.random() <= 0.1 and self.timestep > 400:
            modified_action[2] = 0.2
        return self.env.step(modified_action)

    def reset(self, seed=None):
        self.timestep = 0
        return self.env.reset()