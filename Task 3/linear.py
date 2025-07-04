import numpy as np

class LinearLayer:
    def __init__(self, input_size, output_size):
        self.W = np.random.randn(output_size, input_size)
        self.B = np.random.randn(output_size, 1)

        self.dW = None
        self.dB = None

    def forward(self, input_data):
        self.input = input_data
        self.output = np.dot(self.W, self.input) + self.B
        return self.output

    def backward(self, output_error):
        self.dW = np.dot(output_error, self.input.T)
        self.dB = output_error
        return np.dot(self.W.T, output_error)

    def update_weights(self, input_data, lr):
        self.W -= lr * self.dW
        self.B -= lr * self.dB
