import gymnasium as gym
from gymnasium import spaces
import numpy as np
from client import Client
from client_w_gui import Client_w_GUI
import numpy as np
import copy
import collections as col
import math

class TorcsEnv(gym.Env):
    def __init__(self, gui=False, infinite=False):
        self.initial = True
        self.gui = gui

        self.terminal_judge_start = 100  # If after 1000 timestep still no progress, terminated
        self.termination_limit_progress = 5  # [km/h], episode terminates if car is running slower than this limit

        if infinite:
            self.terminal_judge_start = 1000000000

        # if gears are enabled how does one include a discrete action in a continuous action space
        self.action_space = gym.spaces.Box(
            low=np.array([-1.0, 0.0, 0.0]),
            high=np.array([1.0, 1.0, 1.0]),
            dtype=np.float32
        )

        high = np.full(23, 1)
        low = np.full(23, 1)
        self.observation_space = spaces.Box(low=low, high=high)

    def step(self, action):
        self.client.R.d['steer'] = action[0]  # in [-1, 1]
        self.client.R.d['accel'] = action[1]
        self.client.R.d['brake'] = action[2]

        self.client.R.d['gear'] = 1
        if self.client.S.d['speedX'] > 50:
            self.client.R.d['gear'] = 2
        if self.client.S.d['speedX'] > 80:
            self.client.R.d['gear'] = 3
        if self.client.S.d['speedX'] > 110:
            self.client.R.d['gear'] = 4
        if self.client.S.d['speedX'] > 140:
            self.client.R.d['gear'] = 5
        if self.client.S.d['speedX'] > 170:
            self.client.R.d['gear'] = 6

        # Save the previous full-obs from torcs for the reward calculation
        obs_pre = copy.deepcopy(self.client.S.d)

        # Apply the Agent's action into torcs
        self.client.respond_to_server()
        # Get the response of TORCS
        self.client.get_servers_input()

        # Get the current full-observation from torcs
        obs = self.client.S.d

        # Make an obsevation from a raw observation vector from TORCS
        self.observation = self.make_observaton(obs)

        # Reward setting
        sp = np.array(obs['speedX'])

        #progress = sp*np.cos(obs['angle']) - np.abs(sp*np.sin(obs['angle'])) - sp*np.abs(obs['trackPos'])
        progress = sp*np.cos(obs['angle']) - sp*max(np.abs(obs['trackPos'])-0.3,0)**2
        #progress = sp*np.cos(obs['angle']) + sp*self.client.R.d['brake'] - (1 - self.observation.track[9])*sp - sp*max(np.abs(obs['trackPos'])-0.3,0)**2
        #progress = sp*np.cos(obs['angle']) - (1 - min(max(self.observation.track[9], 0), 1))*sp - sp*max(np.abs(obs['trackPos'])-0.3,0)**2
        reward = progress

        # collision detection
        if obs['damage'] - obs_pre['damage'] > 0:
            reward = -1
            self.client.R.d['meta'] = True

        #Episode is terminated if the car is out of track
        if abs(obs['trackPos']) > 1:
            reward = -1
            self.client.R.d['meta'] = True

        if np.cos(obs['angle']) < 0: # Episode is terminated if the agent runs backward
            reward = -1
            self.client.R.d['meta'] = True

        if self.terminal_judge_start < self.time_step:
            if progress < self.termination_limit_progress:
                self.client.R.d['meta'] = True
        
        if self.time_step > self.client.maxSteps:
            self.client.R.d['meta'] = True

        if self.client.R.d['meta'] is True: # Send a reset signal
            self.client.respond_to_server()

        self.time_step += 1
        ob = self.observation
        state = np.hstack((ob.angle, ob.track, ob.trackPos, ob.speedX, ob.speedY))

        return state, reward, self.client.R.d['meta'], self.client.R.d['meta'], {}

    def reset(self, seed=None):
        if self.initial:
            if self.gui:
                self.client = Client_w_GUI()
            else:
                self.client = Client()
            self.initial = False
        else:
            self.client.R.d['meta'] = True
            self.client.respond_to_server()

        self.time_step = 0

        self.client.get_servers_input()  # Get the initial input from torcs

        self.observation = self.make_observaton(self.client.S.d)

        ob = self.observation
        state = np.hstack((ob.angle, ob.track, ob.trackPos, ob.speedX, ob.speedY)) # maybe add wheel spin vel back for controlling sliding

        return state, None
    
    def close(self):
        self.client.shutdown()

    def make_observaton(self, raw_obs):
        names = ['focus',
                    'speedX', 'speedY', 'speedZ', 'angle', 'damage',
                    'opponents',
                    'rpm',
                    'track',
                    'trackPos',
                    'wheelSpinVel']

        Observation = col.namedtuple('Observaion', names)
        return Observation(focus=np.array(raw_obs['focus'], dtype=np.float32)/200.,
                            speedX=np.array(raw_obs['speedX'], dtype=np.float32)/300.0,
                            speedY=np.array(raw_obs['speedY'], dtype=np.float32)/300.0,
                            speedZ=np.array(raw_obs['speedZ'], dtype=np.float32)/300.0,
                            angle=np.array(raw_obs['angle'], dtype=np.float32)/math.pi,
                            damage=np.array(raw_obs['damage'], dtype=np.float32),
                            opponents=np.array(raw_obs['opponents'], dtype=np.float32)/200.,
                            rpm=np.array(raw_obs['rpm'], dtype=np.float32)/10000,
                            track=np.array(raw_obs['track'], dtype=np.float32)/200.,
                            trackPos=np.array(raw_obs['trackPos'], dtype=np.float32)/1.,
                            wheelSpinVel=np.array(raw_obs['wheelSpinVel'], dtype=np.float32))