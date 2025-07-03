import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QMessageBox, QStatusBar)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


# MatplotlibCanvas Class to integrate Matplotlib with PyQt5
class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        super().__init__(self.fig)
        self.setParent(parent)

    # Function to plot the generated data
    def plot_data(self, data0x, data0y, data1x, data1y):
        self.ax.clear()


        # Function to represent points in the chart (class 0)
        self.ax.scatter(data0x, data0y, color = 'blue', label = 'Class 0', alpha = 0.6)

        # class 1
        self.ax.scatter(data1x, data1y, color = 'red', label = 'Class 1', alpha = 0.6)

        # Set plot labels and legend
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.set_title("Generated Data Samples")
        self.ax.legend()

        # Redraw the canvas
        self.draw()


# Main Window Class
class DataGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle('Gaussian Data Generator')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")  # Set background color

        # Layouts
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Set margins
        layout.setSpacing(15)  # Set spacing between elements

        # Add the Matplotlib canvas
        self.canvas = MatplotlibCanvas(self)
        layout.addWidget(self.canvas)

        # Modes per class input
        modes_layout = QHBoxLayout()
        self.modes_label = QLabel('Modes per Class:')
        self.modes_input = QLineEdit(self)
        self.modes_input.setText('2')  # Default value
        self.modes_input.setFixedWidth(60)  # Fixed width for the input
        modes_layout.addWidget(self.modes_label)
        modes_layout.addWidget(self.modes_input)

        # Samples per mode input
        samples_layout = QHBoxLayout()
        self.samples_label = QLabel('Samples per Mode:')
        self.samples_input = QLineEdit(self)
        self.samples_input.setText('100')  # Default value
        self.samples_input.setFixedWidth(60)  # Fixed width for the input
        samples_layout.addWidget(self.samples_label)
        samples_layout.addWidget(self.samples_input)

        # Generate button
        self.generate_button = QPushButton('Generate Data')
        self.generate_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")  # Button styling
        self.generate_button.clicked.connect(self.generate_data)  # Connect the button click to generate data
        layout.addLayout(modes_layout)
        layout.addLayout(samples_layout)
        layout.addWidget(self.generate_button)

        # Status Bar
        self.status_bar = QStatusBar()
        layout.addWidget(self.status_bar)

        self.setLayout(layout)

    # Function to generate data
    def generate_data(self):
        try:
            modes = int(self.modes_input.text())
            samples_per_mode = int(self.samples_input.text())
            if modes <= 0 or samples_per_mode <= 0:
                raise ValueError("Please enter positive integers.")


            # Generate the data
            data0x = []
            data0y = []
            data1x = []
            data1y = []


            modes_per_class = int(self.modes_input.text())
            samples_per_mode = int(self.samples_input.text())



            # External loop (2 loops, one for each class)
            for i in range(2):
                for j in range(modes_per_class):
                    
                    # We calculate a random mean and a random variance for x and y

                    mean_x = np.random.uniform(0, 100)
                    mean_y = np.random.uniform(0, 100)

                    variance_x = np.random.uniform(0, 100)
                    variance_y = np.random.uniform(0, 100)

                    for k in range(samples_per_mode):
                        # Creating random coordinate using normal distribution with given mean and variance
                        x = np.random.normal(loc=mean_x, scale=np.sqrt(variance_x))
                        y = np.random.normal(loc=mean_y, scale=np.sqrt(variance_y))

                        if (i == 0):
                            data0x.append(x)
                            data0y.append(y)
                        else:
                            data1x.append(x)
                            data1y.append(y)


            self.canvas.plot_data(data0x, data0y, data1x, data1y)



        except ValueError as e:
            QMessageBox.critical(self, "Input Error", str(e))


# Main function to run the application
def main():
    app = QApplication(sys.argv)
    main_window = DataGeneratorApp()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
