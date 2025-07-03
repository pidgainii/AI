from linear import Linear
from sigmoid import Sigmoid
from softmax import Softmax
import numpy as np

class NeuralNetwork:

    def __init__(self, input_width, hidden_width, hidden_depth, learning_rate, epochs):
        self.learning_rate = learning_rate
        self.epochs = epochs

        self.layers = []

        self.layers.append(Linear(2, input_width))
        self.layers.append(Sigmoid())

        width = input_width

        for i in range(hidden_depth):
            self.layers.append(Linear(width, hidden_width))
            self.layers.append(Sigmoid())

            width = hidden_width
        
        # depth of the output layer is 2
        self.layers.append(Linear(width, 2))
        self.layers.append(Sigmoid())


    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def backward(self, grad):
        for layer in reversed(self.layers):
            grad = layer.backward(grad)

    def adjust(self, learning_rate):
        for layer in self.layers:
            layer.adjust(learning_rate)



    # Training function for the Neuron
    def training(self, data0, data1):
        for e in range(self.epochs):


            # Shuffle the data for each class separately
            np.random.shuffle(data0)
            np.random.shuffle(data1)

            for i in range(len(data1)):
                self.train(data0[i][0], data0[i][1], 0)
                self.train(data1[i][0], data1[i][1], 1)


    def train(self, x, y, class_label):
        # primero hacemos el forward, calculamos el error.
        # hacemos el backward, y por ultimo el adjust

        prediction = self.forward((x, y))


        grad0 = prediction[0] - class_label
        grad1 = prediction[1] - class_label


        grad = np.array([grad0, grad1])
        

        self.backward(grad)

        self.adjust(self.learning_rate)

    def predict(self, x, y):
        return self.forward((x, y))