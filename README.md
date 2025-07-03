# AI Beginner Tasks  
Understanding the behavior of a Single Neuron (Perceptron), Shallow Neural Networks, Search Algorithms, and Fuzzy Control  

# Task 1: Gaussian Data Generator

This Python desktop application allows you to generate and visualize 2D data samples drawn from Gaussian (normal) distributions, organized by classes and modes.

## 📌 Description

The program generates synthetic data simulating two distinct classes, each with multiple modes (distribution centers). Points are generated using a normal distribution with random means and variances for each mode. The results are dynamically displayed on an integrated plot using Matplotlib and PyQt5.

## 🛠️ Technologies Used

- **Python 3**
- **PyQt5** – for the graphical user interface
- **Matplotlib** – for data visualization
- **NumPy** – for random data generation

## 🎮 How to Use

1. **Modes per class**: Set how many modes each class will have (e.g., 2).  
2. **Samples per mode**: Set how many data points to generate per mode.  
3. Click **"Generate Data"** to create and visualize the samples.

Blue points represent Class 0, and red points represent Class 1.

## 📸 Screenshot

![Task 1 Screenshot](Screenshots/task1screenshot.png)



# Task 2: Gaussian Data Generator with Single Neuron Training

This Python desktop application extends Task 1 by adding a single neuron (perceptron) that learns to classify the generated Gaussian data. The neuron uses various activation functions (default: Heaviside) and plots the decision boundary after training.

## 📌 Description

The program generates synthetic data similar to Task 1, then trains a single neuron to separate the two classes. It visualizes the data points along with the neuron's decision boundary and background coloring indicating the classified regions.

## 🛠️ Technologies Used

- **Python 3**
- **PyQt5** – for the graphical user interface
- **Matplotlib** – for data visualization
- **NumPy** – for random data generation and neuron computations

## 🎮 How to Use

1. **Modes per class**: Set how many modes each class will have (e.g., 2).  
2. **Samples per mode**: Set how many data points to generate per mode.  
3. Click **"Generate Data and Train Neuron"** to create and visualize the samples.

Blue points represent Class 0, red points represent Class 1, and the green dashed line shows the neuron's decision boundary.

## 📸 Screenshot

![Task 2 Screenshot](Screenshots/task2screenshot.png)
