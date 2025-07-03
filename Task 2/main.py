import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QMessageBox, QStatusBar)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# Define the Neuron class
class Neuron:
    def __init__(self, learning_rate=0.01, epochs=2000, activation='heaviside'):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.activation_name = activation
        self.weightX = None
        self.weightY = None
        self.bias = 0  # Adding a bias term

    # Function that includes all activation functions
    def activation(self, z):
        if self.activation_name == 'heaviside':
            return np.where(z >= 0, 1, 0)
        elif self.activation_name == 'sigmoid':
            return 1 / (1 + np.exp(-z))
        elif self.activation_name == 'sin':
            return np.sin(z)
        elif self.activation_name == 'tanh':
            return np.tanh(z)
        elif self.activation_name == 'sign':
            return np.sign(z)
        elif self.activation_name == 'relu':
            return np.maximum(0, z)
        elif self.activation_name == 'leaky_relu':
            return np.where(z > 0, z, 0.01 * z)

    # Derivative of the activation function
    def activation_derivative(self, z):
        if self.activation_name == 'sigmoid':
            return self.activation(z) * (1 - self.activation(z))
        elif self.activation_name == 'tanh':
            return 1 - np.tanh(z) ** 2
        elif self.activation_name == 'relu':
            return np.where(z > 0, 1, 0)
        elif self.activation_name == 'leaky_relu':
            return np.where(z > 0, 1, 0.01)
        else:
            return 1

    # Training function for the Neuron
    def training(self, data0, data1):
        self.weightX = np.random.normal(loc=0.0, scale=1)
        self.weightY = np.random.normal(loc=0.0, scale=1)
        self.bias = np.random.normal(loc=0.0, scale=1)  # Initialize bias

        for e in range(self.epochs):
            for i in range(len(data1)):
                self.train(data0[i][0], data0[i][1], 0)
                self.train(data1[i][0], data1[i][1], 1)

    def train(self, x, y, true_value):
        prediction = self.predict(x, y)
        s = self.weightX * x + self.weightY * y + self.bias
        derivative = self.activation_derivative(s)
        aux = self.learning_rate * (true_value - prediction)
        self.weightX += aux * derivative * x
        self.weightY += aux * derivative * y
        self.bias += aux * derivative  # Update bias term

    def predict(self, x, y):
        z = x * self.weightX + y * self.weightY + self.bias
        return self.activation(z)

# MatplotlibCanvas Class to integrate Matplotlib with PyQt5
class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        super().__init__(self.fig)
        self.setParent(parent)

    def plot_data(self, data0x, data0y, data1x, data1y, neuron=None):
        self.ax.clear()
        self.ax.scatter(data0x, data0y, color='blue', label='Class 0', alpha=0.6)
        self.ax.scatter(data1x, data1y, color='red', label='Class 1', alpha=0.6)
        
        if neuron and neuron.weightX is not None and neuron.weightY is not None:
            x_vals = np.array(self.ax.get_xlim())
            y_vals = -(neuron.weightX * x_vals + neuron.bias) / neuron.weightY  # Adjust for bias
            self._fill_background(neuron)
            self.ax.plot(x_vals, y_vals, '--', color="green", label="Decision Boundary")

        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.set_title("Generated Data Samples and Decision Boundary")
        self.ax.legend()
        self.draw()

    def _fill_background(self, neuron):
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()
        x_min -= 10
        x_max += 10
        y_min -= 10
        y_max += 10

        x_grid, y_grid = np.meshgrid(np.linspace(x_min, x_max, 500),
                                     np.linspace(y_min, y_max, 500))
        
        z_vals = neuron.weightX * x_grid + neuron.weightY * y_grid + neuron.bias
        self.ax.contourf(x_grid, y_grid, z_vals, levels=[-np.inf, 0, np.inf], colors=['blue', 'red'], alpha=0.3)

# Main Window Class
class DataGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Gaussian Data Generator with Neuron')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.canvas = MatplotlibCanvas(self)
        layout.addWidget(self.canvas)

        modes_layout = QHBoxLayout()
        self.modes_label = QLabel('Modes per Class:')
        self.modes_input = QLineEdit(self)
        self.modes_input.setText('2')
        self.modes_input.setFixedWidth(60)
        modes_layout.addWidget(self.modes_label)
        modes_layout.addWidget(self.modes_input)

        samples_layout = QHBoxLayout()
        self.samples_label = QLabel('Samples per Mode:')
        self.samples_input = QLineEdit(self)
        self.samples_input.setText('100')
        self.samples_input.setFixedWidth(60)
        samples_layout.addWidget(self.samples_label)
        samples_layout.addWidget(self.samples_input)

        self.generate_button = QPushButton('Generate Data and Train Neuron')
        self.generate_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.generate_button.clicked.connect(self.generate_data_and_train)
        layout.addLayout(modes_layout)
        layout.addLayout(samples_layout)
        layout.addWidget(self.generate_button)

        self.status_bar = QStatusBar()
        layout.addWidget(self.status_bar)

        self.setLayout(layout)

    def generate_data_and_train(self):
        try:
            modes_per_class = int(self.modes_input.text())
            samples_per_mode = int(self.samples_input.text())

            if modes_per_class <= 0 or samples_per_mode <= 0:
                raise ValueError("Please enter positive integers.")

            data0x, data0y, data1x, data1y = [], [], [], []

            for i in range(2):
                for j in range(modes_per_class):
                    mean_x = np.random.uniform(0, 100)
                    mean_y = np.random.uniform(0, 100)
                    variance_x = np.random.uniform(0, 100)
                    variance_y = np.random.uniform(0, 100)

                    for _ in range(samples_per_mode):
                        x = np.random.normal(loc=mean_x, scale=np.sqrt(variance_x))
                        y = np.random.normal(loc=mean_y, scale=np.sqrt(variance_y))

                        if i == 0:
                            data0x.append(x)
                            data0y.append(y)
                        else:
                            data1x.append(x)
                            data1y.append(y)

            data0 = [[x, y] for x, y in zip(data0x, data0y)]
            data1 = [[x, y] for x, y in zip(data1x, data1y)]

            neuron = Neuron(learning_rate=0.1, epochs=2000, activation='heaviside')
            neuron.training(data0, data1)

            self.canvas.plot_data(data0x, data0y, data1x, data1y, neuron=neuron)

        except ValueError as e:
            QMessageBox.critical(self, "Input Error", str(e))

def main():
    app = QApplication(sys.argv)
    main_window = DataGeneratorApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
