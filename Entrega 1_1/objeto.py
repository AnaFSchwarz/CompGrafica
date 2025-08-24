from abc import ABC, abstractmethod

class ObjetoGrafico(ABC):
    def __init__(self, pontos):
        self.pontos = pontos  # lista de pontos no mundo

    @abstractmethod
    def desenhar(self, canvas, window, viewport):
        pass
