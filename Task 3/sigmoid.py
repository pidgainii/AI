import numpy as np
from layer import Layer  # Import the abstract Layer class

class Sigmoid(Layer):
    def __init__(self):
        self.cache = None  # To store the input to the activation function

    def forward(self, x):
        self.cache = x
        return 1 / (1 + np.exp(-x))  # Sigmoid activation function

    def backward(self, grad):
        output = 1 / (1 + np.exp(-self.cache))  # Recompute sigmoid output from cache
        sigmoid_derivative = output * (1 - output)
        return grad * sigmoid_derivative


    def adjust(self, learning_rate):
        pass  # No learnable parameters in activation functions
