from abc import ABC, abstractmethod
import numpy as np
import math

class ObjetoGrafico(ABC):
    def __init__(self, pontos, cor, window):
        self.pontos = [(x/100, y/100) for (x, y) in pontos]
        self.cor = cor
        self.window = window

    @abstractmethod
    def desenhar(self, canvas, window, scn, viewport):
        pass
    
    def centro(self):
        xs = [p[0] for p in self.pontos]
        ys = [p[1] for p in self.pontos]
        return sum(xs)/len(xs), sum(ys)/len(ys)
    
    def multiplicacao_matrizes(self, Matriz):
        novos_pontos = []
        for (x, y) in self.pontos:
            # ponto como vetor linha
            ponto_h = np.array([x, y, 1])
            # multiplica ponto linha @ matriz
            ponto_trans = ponto_h @ Matriz
            novos_pontos.append((ponto_trans[0], ponto_trans[1]))
        
        self.pontos = novos_pontos
         
    def transladar(self, dx, dy):
        T = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [dx, dy, 1]
        ])
        self.multiplicacao_matrizes(T)
        
    def escalonar(self, sx, sy):
        if not self.pontos:
            return

        if sy is None:
            sy = sx

        cx, cy = self.centro()

        # translação para origem
        T1 = np.array([ [1, 0, 0],
                        [0, 1, 0],
                        [-cx, -cy, 1]], dtype=float)
        
        # translação de volta
        T2 = np.array([ [1, 0, 0],
                        [0, 1, 0],
                        [cx, cy, 1]], dtype=float)

        # escalonamento
        S  = np.array([[sx, 0,  0],
                       [0,  sy, 0],
                       [0,  0,  1]], dtype=float)
        

        M = T1 @ S @ T2
        self.multiplicacao_matrizes(M)

    def rotacionar(self, angulo, cx=0, cy=0):
        rad = math.radians(angulo)

        R = np.array([
            [math.cos(rad), -math.sin(rad), 0],
            [math.sin(rad),  math.cos(rad), 0],
            [0, 0, 1]
        ])

        # translação para origem
        T1 = np.array([ [1, 0, 0],
                        [0, 1, 0],
                        [-cx, -cy, 1]], dtype=float)

        # translação de volta
        T2 = np.array([ [1, 0, 0],
                        [0, 1, 0],
                        [cx, cy, 1]], dtype=float)

        # matriz resultante: T2 * R * T1
        M = T1 @ R @ T2

        self.multiplicacao_matrizes(M)


    def rotacao_window(self,x, y):

        tetha = math.radians(self.window.angulo)
        cos_a = math.cos(tetha)
        sin_a = math.sin(tetha)

        xr = x * cos_a - y * sin_a
        yr = x * sin_a + y * cos_a
        return xr, yr