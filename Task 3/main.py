import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from neural_network import NeuralNetwork  # Assuming you have this implemented

# Streamlit App
st.title("Data Generation and Neural Network Classification")

# Input parameters
modes_per_class = st.number_input("Number of Modes per Class", min_value=1, value=2, step=1)
samples_per_mode = st.number_input("Number of Samples per Mode", min_value=1, value=50, step=1)

# Generate button
if st.button("Generate and Classify"):
    # Data generation
    data0x, data0y, data1x, data1y = [], [], [], []
    for i in range(2):  # Two classes
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

    # Create Neural Network
    input_layer_width = 2  # Two inputs: x and y
    hidden_layer_width = 3
    hidden_layer_depth = 3
    learning_rate = 0.0001
    epochs = 450

    # Output size 2 (for two classes)
    neuron = NeuralNetwork(input_layer_width, hidden_layer_width, hidden_layer_depth, learning_rate, epochs)
    neuron.training(data0, data1)



    # Generate grid for visualization
    x_min, x_max = min(min(data0x), min(data1x)) - 10, max(max(data0x), max(data1x)) + 10
    y_min, y_max = min(min(data0y), min(data1y)) - 10, max(max(data0y), max(data1y)) + 10
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))

    # Predict class for each point in the grid
    grid_points = np.c_[xx.ravel(), yy.ravel()]
    predictions = np.array([neuron.predict(p[0], p[1]) for p in grid_points])  # Each prediction is a 2-element array

    # Use only the first neuron's output directly
    predicted_classes = (predictions[:, 0] > 0.5).astype(int)  # Classify based on a threshold (e.g., 0.5)
    predicted_classes = predicted_classes.reshape(xx.shape)



    # Plot results
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.contourf(xx, yy, predicted_classes, alpha=0.5, cmap="RdBu_r")  # Red for Class 0, Blue for Class 1
    ax.scatter(data0x, data0y, color="blue", label="Class 0")  # Blue for Class 0
    ax.scatter(data1x, data1y, color="red", label="Class 1")  # Red for Class 1

    ax.legend()
    ax.set_title("Data and Classification Boundary")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    st.pyplot(fig)
