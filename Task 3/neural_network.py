import numpy as np
from linear import LinearLayer
from activation import ActivationLayer

class SimpleNeuralNet:
    def __init__(self, inputs, neurons_per_hidden, hidden_layers, act_func='sigmoid', lr=0.1, iterations=400):
        self.lr = lr
        self.iterations = iterations
        self.layers = []

        # Configuración de la arquitectura
        structure = [inputs] + [neurons_per_hidden] * hidden_layers + [2]
        for idx in range(len(structure) - 1):
            self.layers.append(LinearLayer(structure[idx], structure[idx + 1]))
            self.layers.append(ActivationLayer(act_func))

    def forward_propagation(self, x):
        activations = [x]
        for layer in self.layers:
            activations.append(layer.forward(activations[-1]))
        return activations

    def backward_propagation(self, x, y):
        activations = self.forward_propagation(x)
        errors = [None] * len(self.layers)

        # Error en la salida
        errors[-1] = activations[-1] - y
        for i in range(len(self.layers) - 1, 0, -1):
            errors[i - 1] = self.layers[i].backward(errors[i])
        self.layers[0].backward(errors[0])

        # Actualizar pesos
        for i, layer in enumerate(self.layers):
            if isinstance(layer, LinearLayer):
                layer.update_weights(activations[i], self.lr)

    def train(self, X, y):
        for _ in range(self.iterations):
            for idx in range(X.shape[0]):
                x_i = X[idx].reshape(-1, 1)
                y_i = np.zeros((2, 1))
                y_i[int(y[idx])] = 1
                self.backward_propagation(x_i, y_i)

    def predict(self, x):
        activations = self.forward_propagation(x.reshape(-1, 1))
        return np.argmax(activations[-1]), activations[-1].flatten()
