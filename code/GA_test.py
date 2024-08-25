from neural_net import NeuralNet
from client_w_gui import Client_w_GUI
import numpy as np
import math

def test_best_bot():
    chromosomes = np.loadtxt("GA/Fitness/chromosomes1.txt")
    agent = NeuralNet(chromosomes[0])
    for step in range(C.maxSteps, 0, -1):
        C.get_servers_input()
        r = agent.drive(C.S, C.R)
        C.update(r)
        if C.S.d['trackPos'] > 1:
            C.R.d['meta'] = True
            C.respond_to_server()
            break
        C.respond_to_server()

def follow_axis():
    for step in range(C.maxSteps, 0, -1):
        C.get_servers_input()
        
        S,R= C.S.d,C.R.d
        target_speed=140
        
        # Steer To Corner
        R['steer']= S['angle']*10 / math.pi
        # Steer To Center
        R['steer']-= S['trackPos']*.20

        # Throttle Control
        if S['speedX'] < target_speed - (R['steer']*50):
            R['accel']+= .01
        else:
            R['accel']-= .01
        if S['speedX']<10:
            R['accel']+= 1/(S['speedX']+.1)

        # Automatic Transmission
        R['gear']=1
        if S['speedX']>50:
            R['gear']=2
        if S['speedX']>80:
            R['gear']=3
        if S['speedX']>110:
            R['gear']=4
        if S['speedX']>140:
            R['gear']=5
        if S['speedX']>170:
            R['gear']=6

        C.respond_to_server()

if __name__ == "__main__":
    C = Client_w_GUI()
    test_best_bot()
    #follow_axis()
    C.shutdown()