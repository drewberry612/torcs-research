import math
import numpy as np

class NeuralNet():
    """
    Acts as an agent
    Instantiated from a chromosome of weights and biases
    """

    # Neural network structure
    ninputs = 23
    nhids = 36
    nouts = 3

    # chromosome properties
    weights_and_bias_shapes = [[ninputs, nhids], [nhids], [nhids, nouts], [nouts]]
    chromosome_length = ninputs*nhids + nhids + nhids*nouts + nouts

    def __init__(self, chromosome):
        weights_and_biases = NeuralNet.convert_vector_to_weights_and_biases(chromosome)
        [self.W1, self.b1, self.W2, self.b2] = weights_and_biases


    def calculate_decision(self, input):
        # run a standard neural network with just one hidden layer, and tanh activation functions everywhere.
        hidden = np.tanh(np.matmul(input, self.W1) + self.b1)
        output = np.tanh(np.matmul(hidden, self.W2) + self.b2)
        
        # outputs
        steer_output = output[0]
        accel_output = output[1] / 2 + 0.5 # rescale it from [-1,1] to [0,1]
        brake_output = output[2] / 2 + 0.5 # rescale it from [-1,1] to [0,1]
        return steer_output, accel_output, brake_output

    @staticmethod    
    def convert_vector_to_weights_and_biases(vec):
        # A useful helper function for converting a flat numpy vector into a list of the 4 weight and bias matrices required.
        # On entry, shapes should be a list e.g. [[4,5],[5],[5,2],[2]] or similar, specifying the shape of each weight/bais matrix in a neural network
        count = 0
        weights_and_biases = []
        for shape in NeuralNet.weights_and_bias_shapes:
            if len(shape) == 2:
                # unpack this chunk into a matrix shape (it must be a weight matrix)
                [m,n] = shape
                s = m*n
                weights_and_biases.append(vec[count:count+s].reshape((m,n)))
                count += s
            else:
                assert len(shape) == 1
                # unpack this chunk into a vector shape (it must be a bias vector)
                [m] = shape
                s = m
                weights_and_biases.append(vec[count:count+s])
                count += s
        assert count==vec.shape[0] # check the vector given was exactly the correct length
        return weights_and_biases
    
    def drive(self, S, R):
        '''
        Drives the agent 
        '''
        s, r = S.d, R.d # sensor and actuator data      
        
        # normalisation
        angle = s['angle'] / math.pi

        track = []
        for i in range(len(s['track'])):
            track.append(s['track'][i] / 200)

        # speed x
        speedX = s['speedX'] / 300

        # speed z
        speedY = s['speedY'] / 300

        input = np.array([angle, s['trackPos']] + list(track) + [speedX, speedY])
        r['steer'], r['accel'], r['brake'] = self.calculate_decision(input)

        # Automatic Transmission
        r['gear'] = 1
        if s['speedX'] > 50:
            r['gear'] = 2
        if s['speedX'] > 80:
            r['gear'] = 3
        if s['speedX'] > 110:
            r['gear'] = 4
        if s['speedX'] > 140:
            r['gear'] = 5
        if s['speedX'] > 170:
            r['gear'] = 6
        
        return r