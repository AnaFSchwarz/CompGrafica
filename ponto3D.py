from objeto3D import ObjetoGrafico3D
import numpy as np

class Ponto3D(ObjetoGrafico3D):
    def __init__(self, x, y, z):
        super().__init__([self])  # o ponto é um "objeto 3D" com ele mesmo
        self.coord = np.array([x, y, z, 1.0])

    def transformar(self, matriz):
        self.coord = matriz @ self.coord

    @property
    def x(self): return self.coord[0]
    @property
    def y(self): return self.coord[1]
    @property
    def z(self): return self.coord[2]

    #def __repr__(self):
    #    return f"Ponto3D({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"
