from objeto3D import ObjetoGrafico3D
import numpy as np

class Ponto3D(ObjetoGrafico3D):
    def __init__(self, x, y, z, cor, window):
        self.cor = cor
        self.window = window
        self.coord = np.array([x, y, z, 1.0])

    def transformar(self, matriz):
        self.coord = matriz @ self.coord

    @property
    def x(self): return self.coord[0]
    @property
    def y(self): return self.coord[1]
    @property
    def z(self): return self.coord[2]

    def desenhar(self, canvas, largura, altura, cor="#00FF00"):
        pass
    