from stable_baselines3 import PPO
from torcs_env import TorcsEnv

"""
Used to test an agent trained by PPO using the graphics
"""

if __name__ == "__main__":
    env = TorcsEnv(True, False) # create a RL environment instance

    model = PPO.load("models/modified_rewards.zip") # load the model using the correct file path

    print(model.policy) # display the neural networks

    state, _ = env.reset() # initialise the environment
    done = False
    while not done:
        action, _ = model.predict(state, deterministic=False) # returns the action based on the state of the game
        state, reward, done, truncated, _ = env.step(action) # advances a timestep