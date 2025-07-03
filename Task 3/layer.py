import numpy as np
from abc import ABC, abstractmethod

# Step 1: Create an Abstract Base Class (ABC) for Layer
class Layer(ABC):
    @abstractmethod
    def forward(self, x):
        pass
    
    @abstractmethod
    def backward(self, grad):
        pass
    
    @abstractmethod
    def adjust(self, learning_rate):
        pass
