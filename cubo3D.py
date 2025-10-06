from ponto3D import Ponto3D
from objeto3D import ObjetoGrafico3D

class Cubo3D(ObjetoGrafico3D):
    def __init__(self, pontos, cor, window, tamanho=1.0):
        # define vértices relativos ao centro
        t = tamanho / 2
        self.window = window
        self.cor = cor
        self.pontos = [
            Ponto3D(-t, -t, -t, self.cor, self.window),
            Ponto3D(t, -t, -t, self.cor, self.window),
            Ponto3D(t, t, -t, self.cor, self.window),
            Ponto3D(-t, t, -t, self.cor, self.window),
            Ponto3D(-t, -t, t, self.cor, self.window),
            Ponto3D(t, -t, t, self.cor, self.window),
            Ponto3D(t, t, t, self.cor, self.window),
            Ponto3D(-t, t, t, self.cor, self.window)
        ]

        self.arestas = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # base inferior
            (4, 5), (5, 6), (6, 7), (7, 4),  # base superior
            (0, 4), (1, 5), (2, 6), (3, 7)   # ligações verticais
        ]

        
        #super().__init__(pontos, arestas)

    def desenhar(self, canvas, largura, altura, cor="#00FF00"):

        def projecao(p):
            # centro do canvas no meio
            x = largura/2 + p.x * 100
            y = altura/2 - p.y * 100
            return (x, y)

        # desenha arestas
        for i, j in self.arestas:
            p1, p2 = self.pontos[i], self.pontos[j]
            x1, y1 = projecao(p1)
            x2, y2 = projecao(p2)
            canvas.create_line(x1, y1, x2, y2, fill=cor, width=2)

        # desenha pontos
        for p in self.pontos:
            x, y = projecao(p)
            canvas.create_oval(x-3, y-3, x+3, y+3, fill="red", outline="black")