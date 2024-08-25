from torcs_env import TorcsEnv
from stable_baselines3 import PPO
from neural_net import NeuralNet
from client import Client
import numpy as np
import csv

def PPO_test(model):
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
    client = Client()
    chromosomes = np.loadtxt(model)
    agent = NeuralNet(chromosomes[0])
    for step in range(client.maxSteps, 0, -1):
        client.get_servers_input()
        r = agent.drive(client.S, client.R)
        client.update(r)
        if client.S.d['trackPos'] > 1:
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
    PPO_models = ["models/model_peak_2_final","models/model_apex_2_final"]
    GA_models = ["GA/Fitness/chromosomes1.txt","GA/Rewards/chromosomes1.txt"]
    
    count = 0
    for m in PPO_models:
        count+=1
        with open(f"distances/PPO{count}.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Experiment', 'Distance'])
        for i in range(10):
            distance = PPO_test(m)
            with open(f"distances/PPO{count}.csv", 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([i, distance])

    count = 0
    for m in GA_models:
        count+=1
        with open(f"distances/GA{count}.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Experiment', 'Distance'])
        for i in range(10):
            distance = GA_test(m)
            with open(f"distances/GA{count}.csv", 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([i, distance])