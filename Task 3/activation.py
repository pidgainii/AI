import numpy as np

class ActivationLayer:
    def __init__(self, activation):
        self.activation = activation
        self.activation_func, self.activation_derivative = self.get_activation_functions(activation)

    def forward(self, input_data):
        self.input = input_data
        self.output = self.activation_func(self.input)
        return self.output

    def backward(self, output_error):
        return output_error * self.activation_derivative(self.output)

    @staticmethod
    def get_activation_functions(name):
        if name == 'sigmoid':
            return lambda x: 1 / (1 + np.exp(-x)), lambda y: y * (1 - y)
        elif name == 'tanh':
            return np.tanh, lambda y: 1 - y ** 2
        elif name == 'relu':
            return lambda x: np.maximum(0, x), lambda y: np.where(y > 0, 1, 0)
        else:
            raise ValueError("Unsupported activation function")
