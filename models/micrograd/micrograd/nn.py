import random
from micrograd.engine import Value

class Module:
    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0
    
    def parameters(self):
        return []
    
class Neuron(Module):

    def __init__(self, nin):
        self.w = [Value(random.uniform(-1, 1)) for _ in range(nin)]
        self.b = Value(random.uniform(-1, 1))
    
    def __call__(self, x):
        act = sum((xi*wi for wi, xi in zip(self.w, x)), self.b)
        return act.tanh()
    
    def parameters(self):
        return [self.b] + self.w

class Layer(Module):

    def __init__(self, nin, nout):
        self.neurons = [Neuron(nin) for _ in range(nout)]
    
    def __call__(self, x):
        outs = [n(x) for n in self.neurons]
        return outs[0] if len(outs) == 1 else outs
    
    def parameters(self):
        return [p for neuron in self.neurons for p in neuron.parameters()]

class MLP(Module):

    def __init__(self, nin, nout):
        layer_dims = [nin] + nout
        self.layers = [Layer(layer_dims[i], layer_dims[i+1]) for i in range(len(nout))]
    
    def __call__(self, x):
        for l in self.layers:
            x = l(x)
        
        return x
    
    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]