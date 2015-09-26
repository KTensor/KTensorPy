import numpy as np;

def sigmoid(x, deriv = False):
    if(deriv == True):
        return x*(1-x)
    else:
        return 1/(1+np.exp(-x))


# class Neuron:
#     def __init__(self, aWeights):
#         '''weights should be a (L+1) vector'''
#         self._weights = aWeights
#
#     def out(self, aInput):
#         '''input should be a weightLength vector, should have a -1 as last value for threshold weight'''
#         return sigmoid(np.dot(aInput, self._weights))


class Layer:
    def __init__(self, numNeurons = 1):
        self._neurons = np.matrix([])
        self._neurLength = numNeurons
        self._weightLength = None
        self._nextLayer = None
        self._prevLayer = None

    def connect(self, layer):
        '''A -> B : B.connect(A)'''
        self._weightLength = layer._neurLength + 1
        # self._neurons = []
        # for i in range(0, self._neurLength):
        #     self._neurons.append(Neuron(2*np.random.random(weightLength) - 1))
        layer._nextLayer = self
        self._prevLayer = layer

    def setNeurons(self, neurarray):
        '''neuron array should be a 2D matrix, rows are neurons, columns are weights, dim is neurLengthxweightLength'''
        self._neurons = neurarray.T

    def getNeurons(self):
        return self._neurons.T

    def out(self, aInput):
        '''input should be a (weightLength - 1) vector'''
        inp = aInput.append(-1)
        # arr = np.array([])
        # for(neuron in self._neurons):
        #     arr.append(neuron.out(inp))
        # return arr
        return inp.dot(self._neurons)


class Input(Layer):
    def __init__(self, length):
        super().__init__(length)

    def out(self, aInput):
        return aInput


class Network:
    def __init__(self, inp, hid, out, layerWeights = None):
        self._input = Input(inp)
        self._output = Layer(out)
        self._layers = []
        self._layers.append(self._input)
        for i in hid:
            self._layers.append(Layer(i))
        self._layers.append(self._output)

        for i in range(1, self._layers.size):
            self._layers[i].connect(self._layers[i-1])
            if layerWeights is None:
                self._layers[i].setNeurons(np.random.rand(self._layers[i]._neurLength, self._layers[i]._weightLength) * 2 - 1)
            else:
                self._layers[i].setNeurons(layerWeights[i-1])

    def out(self, aInput):
        arr = aInput
        for layer in self._layers:
            arr = layer.out(arr)
        return arr

    def train(self):
        pass
'''
To do:
- training, backpropagation
- genetic algorithm
'''
