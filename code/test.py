from stable_baselines3 import PPO
from torcs_env import TorcsEnv

if __name__ == "__main__":
    env = TorcsEnv(True, False)

    model = PPO.load("models/model_peak_2_final")

    print(model.policy)

    state, _ = env.reset()
    done = False
    while not done:
        action, _ = model.predict(state, deterministic=False)
        state, reward, done, truncated, _ = env.step(action)