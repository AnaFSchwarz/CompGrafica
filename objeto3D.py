import numpy as np
from math import cos, sin, radians
from abc import ABC, abstractmethod


class ObjetoGrafico3D(ABC):
    def __init__(self, pontos, cor, arestas, window, tipo_objeto = "3D", tipo_clipping = 1):
        self.pontos = [(x/100, y/100, z/100) for (x, y, z) in pontos]
        self.cor = cor
        self.tipo_clipping = tipo_clipping
        self.window = window
        self.tipo_objeto = tipo_objeto
        self.arestas = arestas

    def desenhar(self, canvas, largura, altura, cor="#00FF00"):
        pass

    #@abstractmethod
    #def clipping(self, pontos, window):
    #    pass

    def _aplicar_transformacao(self, matriz):
        novos_pontos = []
        for (x,y,z) in self.pontos:
            ponto_h = np.array([x,y,z,1])
            ponto_trans = (matriz @ ponto_h)
            novos_pontos.append((ponto_trans[0], ponto_trans[1], ponto_trans[2]))
        self.pontos = novos_pontos

    def transladar(self, dx, dy, dz=0):
        matriz = np.array([
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ])
        self._aplicar_transformacao(matriz)

    def escalonar(self, sx, sy, sz=0):
        matriz = np.array([
            [sx, 0,  0,  0],
            [0,  sy, 0,  0],
            [0,  0,  sz, 0],
            [0,  0,  0,  1]
        ])
        self._aplicar_transformacao(matriz)

    def centro(self):
        xs = [p[0] for p in self.pontos]
        ys = [p[1] for p in self.pontos]
        zs = [p[2] for p in self.pontos]
        return sum(xs)/len(xs), sum(ys)/len(ys), sum(zs)/len(zs)

    def rotacionar(self, angulo, cx, cy, cz):

        a = radians(angulo)

        # Matrizes de rotação para cada eixo
        Rx = np.array([
            [1, 0,      0,       0],
            [0, cos(a), -sin(a), 0],
            [0, sin(a), cos(a),  0],
            [0, 0,      0,       1]
        ], dtype=float)

        Ry = np.array([
            [cos(a),  0, sin(a), 0],
            [0,        1, 0,       0],
            [-sin(a), 0, cos(a), 0],
            [0,        0, 0,       1]
        ], dtype=float)

        Rz = np.array([
            [cos(a), -sin(a), 0, 0],
            [sin(a),  cos(a), 0, 0],
            [0,        0,       1, 0],
            [0,        0,       0, 1]
        ], dtype=float)

        # Matriz de translação para mover para origem e retornar
        T_origem = np.array([
            [1, 0, 0, -cx],
            [0, 1, 0, -cy],
            [0, 0, 1, -cz],
            [0, 0, 0, 1]
        ], dtype=float)

        T_volta = np.array([
            [1, 0, 0, cx],
            [0, 1, 0, cy],
            [0, 0, 1, cz],
            [0, 0, 0, 1]
        ], dtype=float)

        # Matriz composta: aplica X depois Y depois Z
        matriz_total = T_volta @ (Rz @ (Ry @ (Rx @ T_origem)))

        # aplica transformação
        self._aplicar_transformacao(matriz_total)


    def projetar_paralela_ortogonal(self):
        """
        Como o VPN deve ser (0,0,1), projetamos 'descartando z'
        Retorna lista de segmentos 2D projetados
        """
        proj = []
        for i, j in self.arestas:
            p1, p2 = self.pontos[i], self.pontos[j]
            proj.append(((p1[0], p1[1]), (p2[0], p2[1])))
        return proj