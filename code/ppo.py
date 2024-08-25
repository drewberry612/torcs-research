from torcs_env import TorcsEnv
from brake_wrapper import RandomBrakeWrapper
from stable_baselines3 import PPO
from callback import SaveModelAndMetricsCallback
from stable_baselines3.common.logger import configure
import time

def ppo(i=0):
    env = TorcsEnv()

    m = str(i)

    with open(f'params/model_{m}_params.txt', 'w') as file:
        file.write(f"gamma: {0.9999}\nlearning rate: default\nn steps: {100000}\nbatch size: {1000}")
        file.write("\nprogress = modified")
        file.write("\nonly g track 1 and only -1 reward losing conditions")

    log_dir = f"logs/{m}"
    logger = configure(log_dir, ["stdout", "csv"])

    model = PPO("MlpPolicy",
                env,
                verbose=1,
                gamma=0.9999,
                n_steps=100000,
                batch_size=1000)
    
    model.set_logger(logger)

    callback = SaveModelAndMetricsCallback(f"models/model_{m}", f"metrics/model_{m}_metrics.csv", f"episodes/model_{m}_episodes.csv")

    model.learn(total_timesteps=1000000, callback=callback)

    env.close()

def ppo_w_random():
    env = TorcsEnv()
    wrapped_env = RandomBrakeWrapper(env)

    m = "mary"

    with open(f'params/model_{m}_params.txt', 'w') as file:
        file.write(f"gamma: {0.9999}\nlearning rate: default\nn steps: {100000}\nbatch size: {1000}")
        file.write("\nprogress = original")
        file.write('\nonly aalborg track with 0.2 random brake after 400 timesteps and only -1 reward losing conditions')

    log_dir = f"logs/{m}"
    logger = configure(log_dir, ["stdout", "csv"])

    model = PPO("MlpPolicy",
                wrapped_env,
                verbose=1,
                n_steps=100000,
                gamma=0.9999,
                batch_size=1000)
    
    model.set_logger(logger)

    callback = SaveModelAndMetricsCallback(f"models/model_{m}", f"metrics/model_{m}_metrics.csv", f"episodes/model_{m}_episodes.csv")

    model.learn(total_timesteps=10000000, callback=callback)

    env.close()

def ppo_w_load(n="_2", o=""):
    env = TorcsEnv()
    #env = RandomBrakeWrapper(env)

    m = "peak" + o
    i = n

    log_dir = f"logs/{m}{i}"
    logger = configure(log_dir, ["stdout", "csv"])

    model = PPO.load(f"models/model_{m}_final", env=env)

    callback = SaveModelAndMetricsCallback(f"models/model_{m}{i}", f"metrics/model_{m}_metrics.csv", f"episodes/model_{m}_episodes.csv", existing=True)

    model.set_logger(logger)

    model.learn(total_timesteps=10000000000, callback=callback)

    env.close()

def ppo_w_grid():
    count = 0
    for gamma in [0.90, 0.95, 0.97, 0.99, 0.995]:
        for lr in [0.0001, 0.0003, 0.001]:
            count += 1

            if count < 11:
                print(f"skip {count}")
                continue
            else:
                with open(f'params/model_{count}_params.txt', 'w') as file:
                    file.write(f"gamma: {gamma}\nlearning rate: {lr}\nn steps: {12000}\nbatch size: {100}")

                env = TorcsEnv()

                log_dir = f"logs/{count}"
                logger = configure(log_dir, ["stdout", "csv"])

                model = PPO("MlpPolicy",
                            env,
                            verbose=1,
                            learning_rate=lr,
                            n_steps=12000,
                            batch_size=100,
                            gamma=gamma)

                callback = SaveModelAndMetricsCallback(f"models/model_{count}", f"metrics/model_{count}_metrics.csv", f"episodes/model_{count}_episodes.csv")

                model.set_logger(logger)

                model.learn(total_timesteps=900000, callback=callback)

                env.close()
                time.sleep(0.1)

if __name__ == "__main__":
    for i in range(2, 11):
        ppo(i)
    #ppo_w_random()
    #ppo_w_load()
    #ppo_w_grid()