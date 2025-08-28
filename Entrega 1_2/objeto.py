from abc import ABC, abstractmethod

class ObjetoGrafico(ABC):
    def __init__(self, pontos):
        self.pontos = pontos  # lista de pontos no mundo

    @abstractmethod
    def desenhar(self, canvas, window, viewport):
        pass

    
    def transladar(self, dx, dy):
        for i, (x, y) in enumerate(self.pontos):
            self.pontos[i] = (x + dx, y + dy)  

    def escalonar(self, canvas):
        pass

    def rotacionar(self, canvas):
        """Rotações:
            Em torno do centro do mundo
            Em torno do centro do objeto
            Em torno de um ponto qualquer (arbitrário)"""
        pass