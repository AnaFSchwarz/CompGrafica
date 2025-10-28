from objeto3D import ObjetoGrafico3D
import numpy as np

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
        #Calcula o polinômio de Bernstein cúbico
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
         #Gera a malha de pontos e arestas para todas as superfícies
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
         #Desenha a superfície usando projeção ortogonal
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
         #Recalcula a malha após transformações nos pontos de controle
        pontos, arestas = self._gerar_malha()
        self.pontos = [(x/100, y/100, z/100) for (x, y, z) in pontos]
        self.arestas = arestas
