from abc import ABC, abstractmethod
import numpy as np

class ObjetoGrafico(ABC):
    def __init__(self, pontos):
        self.pontos = pontos  # lista de pontos no mundo

    @abstractmethod
    def desenhar(self, canvas, window, viewport):
        pass

    
    # def transladar(self, dx, dy):
    #     for i, (x, y) in enumerate(self.pontos):
    #         self.pontos[i] = (x + dx, y + dy) 
     
    def transladar(self, dx, dy):
    # matriz de translação homogênea
        T = np.array([
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]
        ])
        self.multiplicacao_matrizes(T)
    
    def multiplicacao_matrizes(self, Matriz):
        novos_pontos = []
        for (x, y) in self.pontos:
            # coordenada homogênea
            ponto_h = np.array([x, y, 1])
            # aplica a matriz
            ponto_trans = Matriz @ ponto_h
            # salva de volta no formato (x, y)
            novos_pontos.append((ponto_trans[0], ponto_trans[1]))
        
        self.pontos = novos_pontos

    def escalonar(self, canvas):
        pass

    def rotacionar(self, canvas):
        """Rotações:
            Em torno do centro do mundo
            Em torno do centro do objeto
            Em torno de um ponto qualquer (arbitrário)"""
        pass