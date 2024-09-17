from torcs_env import TorcsEnv
from stable_baselines3 import PPO
from neural_net import NeuralNet
from client import Client
import numpy as np
import csv

"""
Used to test the final models to compare their performance in a graph
"""

def PPO_test(model):
    """
    Test the given PPO model until a time limit or early stopping and return the distance raced
    """

    env = TorcsEnv(False, False)
    model = PPO.load(model)

    state, _ = env.reset()
    done = False
    while not done:
        action, _ = model.predict(state, deterministic=False)
        state, reward, done, truncated, _ = env.step(action)

    env.close()

    return env.client.S.d['distRaced']

def GA_test(model):
    """
    Test the given GA model until a time limit or early stopping and return the distance raced
    """

    client = Client() # Execute the game and create a connection
    chromosomes = np.loadtxt(model)
    agent = NeuralNet(chromosomes[0]) # create the model from the chromosome

    for step in range(client.maxSteps, 0, -1): # run the agent for a certain number of timesteps
        client.get_servers_input()
        r = agent.drive(client.S, client.R)
        client.update(r)

        if client.S.d['trackPos'] > 1: # early stopping criteria for out of bounds
            distance = client.S.d['distRaced']
            client.R.d['meta'] = True
            client.respond_to_server()
            client.shutdown()
            return distance
        
        client.respond_to_server()

    distance = client.S.d['distRaced']
    client.shutdown()
    return distance

if __name__ == "__main__":
    PPO_models = ["models/original_rewards","models/modified_rewards"]
    GA_models = ["models/simple_fitness/chromosomes.txt","models/accumulated_fitness/chromosomes.txt"]
    
    count = 0 # counter for model number
    for m in PPO_models:
        count += 1
        # create csv for the model
        with open(f"distances/PPO{count}.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Experiment', 'Distance'])

        for i in range(10):
            distance = PPO_test(m) # test the agent and record the distance raced
            with open(f"distances/PPO{count}.csv", 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([i, distance])

    count = 0
    for m in GA_models:
        count += 1
        # create csv for the model
        with open(f"distances/GA{count}.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Experiment', 'Distance'])

        for i in range(10):
            distance = GA_test(m) # test the agent and record the distance raced
            with open(f"distances/GA{count}.csv", 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([i, distance])