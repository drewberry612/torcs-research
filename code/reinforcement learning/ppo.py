from torcs_env import TorcsEnv
from brake_wrapper import RandomBrakeWrapper
from stable_baselines3 import PPO
from callback import SaveModelAndMetricsCallback
from stable_baselines3.common.logger import configure
import time

"""
Run to conduct a PPO experiment
The four methods allow for different types of experiment
Other parameters must be hard coded
"""

def ppo(i=0):
    """
    Basic PPO experiment
    """

    env = TorcsEnv()
    m = str(i) # model name

    # save a text file of parameters and other notes for experiment tracking
    with open(f'params/model_{m}_params.txt', 'w') as file:
        file.write(f"gamma: {0.9999}\nlearning rate: default\nn steps: {100000}\nbatch size: {1000}")
        file.write("\nprogress = modified")
        file.write("\nonly g track 1 and only -1 reward losing conditions")

    # create a logger
    log_dir = f"logs/{m}"
    logger = configure(log_dir, ["stdout", "csv"])

    # create the model
    model = PPO("MlpPolicy",
                env,
                verbose=1,
                gamma=0.9999,
                n_steps=100000,
                batch_size=1000)
    
    model.set_logger(logger)
    callback = SaveModelAndMetricsCallback(f"models/model_{m}", f"metrics/model_{m}_metrics.csv", f"episodes/model_{m}_episodes.csv")
    
    # Runs the agent in the environment while it learns
    model.learn(total_timesteps=1000000, callback=callback)

    env.close()

def ppo_w_random():
    """
    Basic PPO experiment but with stochastic brake
    """

    env = TorcsEnv()
    wrapped_env = RandomBrakeWrapper(env)
    m = "a" # model name

    # save a text file of parameters and other notes for experiment tracking
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
    """
    Load a model and continue training
    """

    env = TorcsEnv()
    # can include the stochastic brake
    #env = RandomBrakeWrapper(env)
    m = "a" + o
    i = n # iteration number for metrics

    log_dir = f"logs/{m}{i}"
    logger = configure(log_dir, ["stdout", "csv"])

    model = PPO.load(f"models/model_{m}_final", env=env) # load the zip file of the given name

    callback = SaveModelAndMetricsCallback(f"models/model_{m}{i}", f"metrics/model_{m}_metrics.csv", f"episodes/model_{m}_episodes.csv", existing=True)
    model.set_logger(logger)

    model.learn(total_timesteps=10000000000, callback=callback)

    env.close()

def ppo_w_grid():
    """
    Conducts a grid search for the specified parameters
    """

    count = 0 # permutation counter
    # can add other parameters or values
    for gamma in [0.90, 0.95, 0.97, 0.99, 0.995]:
        for lr in [0.0001, 0.0003, 0.001]:
            count += 1

            if count < 0: # if there is a crash issue, use this to skip permutations already done
                print(f"skip {count}")
                continue
            else:
                # save the models parameters
                with open(f'params/model_{count}_params.txt', 'w') as file:
                    file.write(f"gamma: {gamma}\nlearning rate: {lr}\nn steps: {12000}\nbatch size: {100}")

                env = TorcsEnv()

                log_dir = f"logs/{count}"
                logger = configure(log_dir, ["stdout", "csv"])

                # create model with current parameter set
                model = PPO("MlpPolicy",
                            env,
                            verbose=1,
                            learning_rate=lr,
                            n_steps=12000,
                            batch_size=100,
                            gamma=gamma)

                callback = SaveModelAndMetricsCallback(f"models/model_{count}", f"metrics/model_{count}_metrics.csv", f"episodes/model_{count}_episodes.csv")
                model.set_logger(logger)

                # timesteps can't be too high if the grid search wants to be conducted in finitie time
                model.learn(total_timesteps=900000, callback=callback)

                env.close()
                time.sleep(0.1)

if __name__ == "__main__":
    ppo()
    #ppo_w_random()
    #ppo_w_load()
    #ppo_w_grid()