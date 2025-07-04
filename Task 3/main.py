import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from neural_network import SimpleNeuralNet

class NeuralNetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Neural Network Configurator")
        self.root.geometry("700x300")  # Smaller configuration window

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TCombobox", font=("Arial", 12))

        self.add_configuration_widgets()

    def add_configuration_widgets(self):
        inputs_frame = ttk.LabelFrame(self.root, text="Network Parameters", padding=10)
        inputs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # First column
        ttk.Label(inputs_frame, text="Modes Class 0:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.modes_0 = ttk.Entry(inputs_frame)
        self.modes_0.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(inputs_frame, text="Modes Class 1:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.modes_1 = ttk.Entry(inputs_frame)
        self.modes_1.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(inputs_frame, text="Samples per Mode:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.samples = ttk.Entry(inputs_frame)
        self.samples.grid(row=2, column=1, padx=5, pady=5)

        # Second column
        ttk.Label(inputs_frame, text="Hidden Layers:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.hidden_layers = ttk.Entry(inputs_frame)
        self.hidden_layers.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(inputs_frame, text="Neurons/Hidden Layer:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.neurons = ttk.Entry(inputs_frame)
        self.neurons.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(inputs_frame, text="Activation Function:").grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.activation = ttk.Combobox(inputs_frame, values=["sigmoid", "tanh", "relu"], state="readonly")
        self.activation.set("sigmoid")
        self.activation.grid(row=2, column=3, padx=5, pady=5)

        # Button
        ttk.Button(inputs_frame, text="Generate and Train", command=self.process).grid(row=3, column=0, columnspan=4, pady=10)

    def create_data(self, n_samples, n_modes, label):
        data = []
        for _ in range(n_modes):
            mean = np.random.uniform(-1, 1, 2)
            cov = np.random.uniform(0.1, 0.5, (2, 2))
            cov = np.dot(cov, cov.T)
            samples = np.random.multivariate_normal(mean, cov, n_samples)
            data.append(samples)
        return np.vstack(data), [label] * len(np.vstack(data))

    def process(self):
        try:
            modes_0 = int(self.modes_0.get())
            modes_1 = int(self.modes_1.get())
            samples = int(self.samples.get())
            layers = int(self.hidden_layers.get())
            neurons = int(self.neurons.get())
            act_func = self.activation.get()

            data_0, labels_0 = self.create_data(samples, modes_0, 0)
            data_1, labels_1 = self.create_data(samples, modes_1, 1)

            X = np.vstack((data_0, data_1))
            y = np.array(labels_0 + labels_1)

            # Model setup and training
            model = SimpleNeuralNet(2, neurons, layers, act_func, lr=0.01, iterations=500)
            model.train(X, y)

            # Open visualization window
            self.open_visualization_window(model, X, y)

        except ValueError:
            messagebox.showerror("Error", "Ensure valid integer inputs!")

    def open_visualization_window(self, model, X, y):
        vis_window = tk.Toplevel(self.root)
        vis_window.title("Visualization")
        vis_window.geometry("800x600")  # Larger visualization window

        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1))

        Z = np.array([model.predict(np.array([a, b]))[0] for a, b in zip(xx.ravel(), yy.ravel())])
        Z = Z.reshape(xx.shape)

        fig, ax = plt.subplots()
        ax.contourf(xx, yy, Z, alpha=0.8, cmap='bwr')
        ax.scatter(X[:, 0], X[:, 1], c=y, cmap='bwr', edgecolors='k')

        canvas = FigureCanvasTkAgg(fig, master=vis_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuralNetApp(root)
    root.mainloop()
