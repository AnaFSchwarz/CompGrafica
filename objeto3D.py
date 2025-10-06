import numpy as np
from math import cos, sin, radians
from abc import ABC, abstractmethod


class ObjetoGrafico3D(ABC):
    def __init__(self, pontos):
        """pontos: lista de objetos Ponto3D"""
        self.pontos = pontos

    # ---------- TRANSFORMAÇÕES BÁSICAS ----------
    def _aplicar_transformacao(self, matriz):
        for p in self.pontos:
            p.transformar(matriz)

    def transladar(self, dx, dy, dz):
        matriz = np.array([
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ])
        self._aplicar_transformacao(matriz)

    def escalar(self, sx, sy, sz):
        matriz = np.array([
            [sx, 0,  0,  0],
            [0,  sy, 0,  0],
            [0,  0,  sz, 0],
            [0,  0,  0,  1]
        ])
        self._aplicar_transformacao(matriz)

    def rotacionar_x(self, angulo):
        a = radians(angulo)
        matriz = np.array([
            [1, 0,      0,     0],
            [0, cos(a), -sin(a), 0],
            [0, sin(a), cos(a),  0],
            [0, 0,      0,     1]
        ])
        self._aplicar_transformacao(matriz)

    def rotacionar_y(self, angulo):
        a = radians(angulo)
        matriz = np.array([
            [cos(a),  0, sin(a), 0],
            [0,       1, 0,      0],
            [-sin(a), 0, cos(a), 0],
            [0,       0, 0,      1]
        ])
        self._aplicar_transformacao(matriz)

    def rotacionar_z(self, angulo):
        a = radians(angulo)
        matriz = np.array([
            [cos(a), -sin(a), 0, 0],
            [sin(a), cos(a),  0, 0],
            [0,      0,       1, 0],
            [0,      0,       0, 1]
        ])
        self._aplicar_transformacao(matriz)

    # ---------- ROTAÇÃO EM TORNO DE EIXO ARBITRÁRIO ----------
    def rotacionar_em_torno_de_eixo(self, p1, p2, angulo):
        a = radians(angulo)
        eixo = np.array([p2.x - p1.x, p2.y - p1.y, p2.z - p1.z])
        eixo = eixo / np.linalg.norm(eixo)
        ux, uy, uz = eixo

        c = cos(a)
        s = sin(a)
        matriz_rot = np.array([
            [c + ux**2 * (1 - c),      ux*uy*(1 - c) - uz*s,  ux*uz*(1 - c) + uy*s, 0],
            [uy*ux*(1 - c) + uz*s,     c + uy**2*(1 - c),     uy*uz*(1 - c) - ux*s, 0],
            [uz*ux*(1 - c) - uy*s,     uz*uy*(1 - c) + ux*s,  c + uz**2*(1 - c),    0],
            [0, 0, 0, 1]
        ])

        trans_origem = np.array([
            [1, 0, 0, -p1.x],
            [0, 1, 0, -p1.y],
            [0, 0, 1, -p1.z],
            [0, 0, 0, 1]
        ])
        trans_volta = np.array([
            [1, 0, 0, p1.x],
            [0, 1, 0, p1.y],
            [0, 0, 1, p1.z],
            [0, 0, 0, 1]
        ])

        matriz_total = trans_volta @ matriz_rot @ trans_origem
        self._aplicar_transformacao(matriz_total)

    #def __repr__(self):
    #    return "\n".join(str(s) for s in self.segmentos)
