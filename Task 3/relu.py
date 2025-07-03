import numpy as np
from layer import Layer  # Import the abstract Layer class

class ReLU(Layer):
    def __init__(self):
        self.cache = None  # To store the input to the activation function

    def forward(self, x):
        self.cache = x
        return np.maximum(0, x)  # ReLU activation function

    def backward(self, grad):
        relu_derivative = (self.cache > 0).astype(float)  # Derivative of ReLU: 1 for positive input, 0 otherwise
        return grad * relu_derivative

    def adjust(self, learning_rate):
        pass  # No learnable parameters in activation functions
