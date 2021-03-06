import ffnet as F
import numpy as np

#Kevin Wang
#github:xorkevin

class ConvLayer(F.Layer):
    def __init__(self, numFilters, stride):
        self._filterLength = numFilters
        self._stride = stride
        self._strideLength = None
        self._depth = None
        self._filters = []
        self._filterWidth = None
        self._inputDim = None
        self._prevLayer = None
        self._nextLayer = None

    def connect(self, layer):
        self._inputDim = (layer._depth, layer._stride, layer._stride)
        self._depth = layer._filterLength
        self._strideLength = layer._stride/(self._stride+1)
        self._filterWidth = layer._stride/self._stride
        self._prevLayer = layer
        layer._nextLayer = self

    def setNeurons(self, neurons):
        '''neurons should be a 2D matrix where row is a filter with length filterWidth**2'''
        filters = list(neurons)
        for f in filters:
            self._filters.append(f.reshape(self._inputDim))

    def getNeurons(self):
        filters = []
        for f in self._filters:
            filters.append(np.ravel(f))
        return np.matrix(filters)

    def out(self, inp):
        '''input should be a 3D array with shape inputDim'''
        output = np.zeros((self._filterLength, self._stride, self._stride))
        x, y, z = output.shape
        for i in range(0, x):
            for j in range(0, y):
                for k in range(0, z):
                    output[i, j, k] = np.sum(np.multiply(inp[:, round(j*self._strideLength):round(j*self._strideLength+self._filterWidth), round(k*self._strideLength):round(k*self._strideLength+self._filterWidth)], self._filters[i]))
        return output

    def __str__(self):
        x = '['
        n = self.getNeurons()
        r,c = n.shape
        for i in range(0, r):
            x += '['
            for j in range(0, c):
                x += str(n[i, j])+','
            x += '],'
        x += ']'
        return x

class ConvInput(ConvLayer):
    def out(self, inp):
        return np.resize(inp, (self._filterLength, self._stride, self._stride))

class ConvNetwork(F.Network):
    def __init__(self, convInp=None, conv=None, inp=None, hid=None, out=None, layerWeights=None, exclusive=None):
        if convInp is not None:
            super().initialize(inp, hid, out, layerWeights, exclusive)
            self.initializeConv(convInp, conv)

    def initializeConv(self, convInp, conv):
        '''convInp is a 2tuple depth and max(dim x, dim y)'''
        self._convInput = ConvInput(convInp[0], convInp[1])
        self._convLayers = []
        for i, j in conv:
            self._convLayers.append(ConvLayer(i, j))
        self._convLayers[0].connect(self._convInput)
        for i in range(1, len(self._convLayers)):
            self._convLayers[i].connect(self._convLayers[i-1])
            #self._convLayers[i].setNeurons()
