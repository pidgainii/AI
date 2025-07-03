import numpy as np
from layer import Layer  # Assuming you have a base Layer class

class Linear(Layer):


    # el input_size nos indica el numero de valores que recibe la neurona
    # el width nos indica el numero de neuronas que tiene la capa
    # pd: no necesitamos saber a cuantas neuronas les vamos a enviar nuestro output, porque es el mismo para todas
    def __init__(self, input_size, width):
        
        # aqui se guardan los datos de entrada que luego seran usados en la funcion backward
        self.input_array = None

        
        # cada neurona necesita un array de pesos, por lo que haremos un array de arrays (matriz)
        # filas -> numero de neuronas que tenemos. En cada fila representa una neurona, y sus columnas son sus pesos.
        # Initialize weight matrix with uniform distribution
        self.weight_matrix = np.random.uniform(
            low=-1 * 3, 
            high=1 * 3, 
            size=(width, input_size)
        )


        # un bias para cada neurona
        self.bias_array = np.random.uniform(low=-1, high=1, size=width)  # Small random values between -0.1 and 0.1


        # declaramos aqui tambien los vectores grad (pesos y bias) ya que necesitaremos almacenarlos en la funcion backward
        self.weight_grad = None
        self.bias_grad = None


    def forward(self, x):
        self.input_array = x  # Save the input for use in the backward pass
        # Linear transformation: x * w + b
        return np.dot(x, self.weight_matrix.T) + self.bias_array

    def backward(self, grad):
        # Store the gradient passed from the next layer (to be used for weight updates)
        
        # Gradient with respect to weights (dw): grad * x.T
        self.weight_grad = np.outer(grad, self.input_array)  # Outer product gives shape (width, input_size)
        
        # Gradient with respect to biases (db): Sum along batch axis (if batch processing is implemented)
        self.bias_grad = grad  # Grad for bias is the same as the incoming gradient

        # Return the gradient w.r.t. input to pass to the previous layer
        return np.dot(grad, self.weight_matrix)  # grad * w.T, passed to the previous layer


    def adjust(self, learning_rate):
        # Update weights and biases using the computed gradients
        self.weight_matrix -= learning_rate * self.weight_grad  # Update weights
        self.bias_array -= learning_rate * self.bias_grad  # Update biases

