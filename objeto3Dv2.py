import numpy as np
from math import cos, sin, radians
from abc import ABC, abstractmethod

class ObjetoGrafico3D(ABC):
    def __init__(self, pontos, cor, arestas, window, tipo_objeto="3D", tipo_clipping=1):
        self.pontos = [(x/100, y/100, z/100) for (x, y, z) in pontos]
        self.cor = cor
        self.tipo_clipping = tipo_clipping
        self.window = window
        self.tipo_objeto = tipo_objeto
        self.arestas = arestas
    
    def desenhar(self, canvas, largura, altura, cor="#00FF00"):
        pass
    
    def _aplicar_transformacao(self, matriz):
        novos_pontos = []
        for (x, y, z) in self.pontos:
            ponto_h = np.array([x, y, z, 1])
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
    
    def escalonar(self, sx, sy, sz=1):
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
        Rx = np.array([
            [1, 0,      0,       0],
            [0, cos(a), -sin(a), 0],
            [0, sin(a), cos(a),  0],
            [0, 0,      0,       1]
        ], dtype=float)
        
        Ry = np.array([
            [cos(a),  0, sin(a), 0],
            [0,       1, 0,      0],
            [-sin(a), 0, cos(a), 0],
            [0,       0, 0,      1]
        ], dtype=float)
        
        Rz = np.array([
            [cos(a), -sin(a), 0, 0],
            [sin(a),  cos(a), 0, 0],
            [0,       0,      1, 0],
            [0,       0,      0, 1]
        ], dtype=float)
        
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
        
        matriz_total = T_volta @ (Rz @ (Ry @ (Rx @ T_origem)))
        self._aplicar_transformacao(matriz_total)
    
    def projetar_paralela_ortogonal(self):
        """Projeção ortogonal descartando z"""
        proj = []
        for i, j in self.arestas:
            p1, p2 = self.pontos[i], self.pontos[j]
            proj.append(((p1[0], p1[1]), (p2[0], p2[1])))
        return proj


class SuperficieBezier(ObjetoGrafico3D):
    """
    Representa uma superfície bicúbica de Bézier.
    A superfície é definida por uma matriz 4x4 de pontos de controle
    e é renderizada como uma malha de retalhos (patches).
    """
    
    def __init__(self, matrizes_controle, cor, window, resolucao=16, tipo_clipping=1):
        """
        matrizes_controle: lista de matrizes 4x4 de pontos de controle
                          Cada matriz representa um retalho da superfície
                          Formato: [[[x,y,z], [x,y,z], ...], ...]
        resolucao: número de subdivisões para renderizar (padrão 16x16)
        """
        self.matrizes_controle = matrizes_controle
        self.resolucao = resolucao
        
        # Gera os pontos e arestas da malha
        pontos, arestas = self._gerar_malha()
        
        super().__init__(pontos, cor, arestas, window, tipo_objeto="BEZIER", tipo_clipping=tipo_clipping)
    
    def _bernstein(self, i, t):
        """Calcula o polinômio de Bernstein cúbico"""
        coefs = [
            [1, 0, 0, 0],
            [-3, 3, 0, 0],
            [3, -6, 3, 0],
            [-1, 3, -3, 1]
        ]
        return sum(coefs[i][j] * (t ** j) for j in range(4))
    
    def _avaliar_bezier(self, matriz_controle, u, v):
        """
        Avalia a superfície de Bézier em (u,v) usando blending functions
        matriz_controle: matriz 4x4 de pontos de controle
        u, v: parâmetros no intervalo [0,1]
        """
        ponto = np.array([0.0, 0.0, 0.0])
        
        # Aplica as funções de Bernstein
        for i in range(4):
            for j in range(4):
                Bu = self._bernstein(i, u)
                Bv = self._bernstein(j, v)
                ponto += Bu * Bv * np.array(matriz_controle[i][j])
        
        return tuple(ponto)
    
    def _gerar_malha(self):
        """Gera a malha de pontos e arestas para todas as superfícies"""
        todos_pontos = []
        todas_arestas = []
        offset = 0
        
        for matriz_controle in self.matrizes_controle:
            pontos_patch = []
            
            # Gera grade de pontos u,v
            for i in range(self.resolucao + 1):
                u = i / self.resolucao
                for j in range(self.resolucao + 1):
                    v = j / self.resolucao
                    ponto = self._avaliar_bezier(matriz_controle, u, v)
                    pontos_patch.append(ponto)
            
            # Gera arestas conectando os pontos
            arestas_patch = []
            for i in range(self.resolucao + 1):
                for j in range(self.resolucao + 1):
                    idx = i * (self.resolucao + 1) + j
                    
                    # Aresta horizontal (direita)
                    if j < self.resolucao:
                        arestas_patch.append((offset + idx, offset + idx + 1))
                    
                    # Aresta vertical (baixo)
                    if i < self.resolucao:
                        arestas_patch.append((offset + idx, offset + idx + self.resolucao + 1))
            
            todos_pontos.extend(pontos_patch)
            todas_arestas.extend(arestas_patch)
            offset += len(pontos_patch)
        
        return todos_pontos, todas_arestas
    
    def desenhar(self, canvas, largura, altura, cor=None):
        """Desenha a superfície usando projeção ortogonal"""
        cor_desenho = cor if cor else self.cor
        
        # Projeta os segmentos
        segmentos = self.projetar_paralela_ortogonal()
        
        # Converte coordenadas normalizadas para pixels
        for (x1, y1), (x2, y2) in segmentos:
            px1 = int((x1 + 1) * largura / 2)
            py1 = int((1 - y1) * altura / 2)
            px2 = int((x2 + 1) * largura / 2)
            py2 = int((1 - y2) * altura / 2)
            
            canvas.create_line(px1, py1, px2, py2, fill=cor_desenho, width=1)
    
    def atualizar_malha(self):
        """Recalcula a malha após transformações nos pontos de controle"""
        pontos, arestas = self._gerar_malha()
        self.pontos = [(x/100, y/100, z/100) for (x, y, z) in pontos]
        self.arestas = arestas


# Exemplo de uso: criando uma superfície de Bézier simples
def criar_superficie_exemplo():
    """Cria uma superfície de Bézier ondulada como exemplo"""
    
    # Define uma matriz 4x4 de pontos de controle
    # Formato: [linha][coluna] = [x, y, z]
    matriz_controle = [
        [
            [-100, -100, 0],
            [-100, -33, 30],
            [-100, 33, 30],
            [-100, 100, 0]
        ],
        [
            [-33, -100, 30],
            [-33, -33, 60],
            [-33, 33, 60],
            [-33, 100, 30]
        ],
        [
            [33, -100, 30],
            [33, -33, 60],
            [33, 33, 60],
            [33, 100, 30]
        ],
        [
            [100, -100, 0],
            [100, -33, 30],
            [100, 33, 30],
            [100, 100, 0]
        ]
    ]
    
    # Cria a superfície com uma única matriz (um retalho)
    window = None  # Substituir pela window do seu sistema
    superficie = SuperficieBezier([matriz_controle], cor="#00FF00", window=window, resolucao=16)
    
    return superficie


def criar_superficie_multiplos_retalhos():
    """Exemplo de superfície com múltiplos retalhos conectados"""
    
    # Primeiro retalho
    matriz1 = [
        [[-150, -100, 0], [-150, -33, 20], [-150, 33, 20], [-150, 100, 0]],
        [[-50, -100, 20], [-50, -33, 50], [-50, 33, 50], [-50, 100, 20]],
        [[50, -100, 20], [50, -33, 50], [50, 33, 50], [50, 100, 20]],
        [[150, -100, 0], [150, -33, 20], [150, 33, 20], [150, 100, 0]]
    ]
    
    # Segundo retalho (conectado ao primeiro)
    matriz2 = [
        [[150, -100, 0], [150, -33, 20], [150, 33, 20], [150, 100, 0]],
        [[250, -100, -20], [250, -33, 10], [250, 33, 10], [250, 100, -20]],
        [[350, -100, -20], [350, -33, 10], [350, 33, 10], [350, 100, -20]],
        [[450, -100, 0], [450, -33, 20], [450, 33, 20], [450, 100, 0]]
    ]
    
    window = None  # Substituir pela window do seu sistema
    superficie = SuperficieBezier([matriz1, matriz2], cor="#FF00FF", window=window, resolucao=16)
    
    return superficie