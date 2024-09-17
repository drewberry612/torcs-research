import gymnasium as gym
import numpy as np
import random

class RandomBrakeWrapper(gym.Wrapper):
    """
    Wraps the custom Gym environment to apply a stochastic brake
    Is compatible with StableBaselines3
    """
    def __init__(self, env):
        super(RandomBrakeWrapper, self).__init__(env)
        self.timestep = 0

    def step(self, action):
        """
        Modifies the brake action given by the RL model
        Has a small chance of occurring with a delay
        """

        self.timestep += 1
        modified_action = np.copy(action)

        if random.random() <= 0.1 and self.timestep > 400: # uses a delay of approximately 8 seconds
            modified_action[2] = 0.2

        return self.env.step(modified_action)

    def reset(self, seed=None):
        self.timestep = 0
        return self.env.reset()