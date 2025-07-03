import numpy as np
from layer import Layer  # Import the abstract Layer class

class Softmax(Layer):
    def __init__(self):
        self.cache = None  # To store the input to the activation function

    def forward(self, x):
        self.cache = x
        # Subtracting max(x) for numerical stability
        exp_values = np.exp(x - np.max(x, axis=-1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=-1, keepdims=True)
        return probabilities

    def backward(self, grad):
        # The gradient of the Softmax function
        # grad: The gradient of the loss with respect to the output
        softmax_output = self.forward(self.cache)  # Get the softmax output
        
        # Compute the Jacobian matrix of the softmax function
        # This is used to compute the derivative of the loss with respect to the inputs
        jacobian_matrix = np.diagflat(softmax_output) - np.outer(softmax_output, softmax_output)
        
        # Multiply the gradient with the Jacobian to get the backpropagated gradient
        return np.dot(jacobian_matrix, grad)

    def adjust(self, learning_rate):
        pass  # No learnable parameters in activation functions like Softmax
