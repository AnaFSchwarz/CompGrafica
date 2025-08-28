from abc import ABC, abstractmethod

class ObjetoGrafico(ABC):
    def __init__(self, pontos):
        self.pontos = pontos  # lista de pontos no mundo

    @abstractmethod
    def desenhar(self, canvas, window, viewport):
        pass

    
    def transladar(self, dx, dy):
        quantidade_pontos = len(self.pontos)
        for i in range(quantidade_pontos):
            self.pontos[i][0] += dx
            self.pontos[i][1] += dy     

    def escalonar(self, canvas):
        pass

    def rotacionar(self, canvas):
        """Rotações:
            Em torno do centro do mundo
            Em torno do centro do objeto
            Em torno de um ponto qualquer (arbitrário)"""
        pass