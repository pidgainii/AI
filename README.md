# AI Beginner Tasks  
Understanding the behavior of a Single Neuron (Perceptron), Shallow Neural Networks, Search Algorithms, and Fuzzy Control  

# Task 1: Gaussian Data Generator

## 📌 Description

The program generates synthetic data simulating two distinct classes, each with multiple modes (distribution centers). Points are generated using a normal distribution with random means and variances for each mode. The results are dynamically displayed on an integrated plot using Matplotlib and PyQt5.

Blue points represent Class 0, and red points represent Class 1.

## 📸 Screenshot

![Task 1 Screenshot](Screenshots/task1screenshot.png)



# Task 2: Gaussian Data Generator with Single Neuron Training

## 📌 Description

The program generates synthetic data similar to Task 1, then trains a single neuron to separate the two classes. It visualizes the data points along with the neuron's decision boundary and background coloring indicating the classified regions.

Blue points represent Class 0, red points represent Class 1, and the green dashed line shows the neuron's decision boundary.

The perceptron receives all the coordinates as the input data, and one by one processes them. It makes a prediction on which class does it think this coordinate belong to. After that, the real label is compared to the prediction, and learning occurs (formula below)

![Task 2 formula](Screenshots/task2.1screenshot.png)

After training for 2000 epochs (adjustable) with learning rate 0.1 (adjustable), the perceptron has learned the necessary parameters to draw the decision boundary

## 📸 Screenshot

![Task 2 Screenshot](Screenshots/task2screenshot.png)
