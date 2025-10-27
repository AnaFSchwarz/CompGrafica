from tkinter import *
from tkinter import messagebox

class Window():
    def __init__(self, xmin=-1, xmax=1, ymin=-1, ymax= 1):
        # estado atual
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

        # estado base (imutável, referência para o zoom)
        self.base_xmin = xmin
        self.base_xmax = xmax
        self.base_ymin = ymin
        self.base_ymax = ymax

        # ângulo de rotação da window
        self.angulo = 0  

    def mover(self, dx, dy):
        self.xmin += dx
        self.xmax += dx
        self.ymin += dy
        self.ymax += dy
    
    def centralizar(self):
        tam = self.get_tam()
        self.xmin = -tam/2
        self.xmax = tam / 2
        self.ymin = -tam / 2
        self.ymax = tam / 2
    
    def get_tam(self):
        tam = self.xmax - self.xmin
        return tam
        
    
    def zoom(self, fator_per):
        """
        Redefine a window a partir do zoom percentual.
        - fator_per = 15  → window original (escala 1.0)
        - fator_per > 15  → zoom out (afasta, aumenta janela)
        - fator_per < 15  → zoom in (aproxima, reduz janela)
        - fator_per = 0   → zoom máximo (reduz bastante a tela)
        """

        largura_base = self.base_xmax - self.base_xmin
        altura_base  = self.base_ymax - self.base_ymin

        # Ajuste: fator_per=25 → fator=1.0
        fator = 1 + ((25 - fator_per) / 100.0)

        # Evita fator zero ou negativo
        if fator <= 0.01:
            fator = 0.01

        largura = largura_base * fator
        altura  = altura_base * fator

        cx = (self.base_xmin + self.base_xmax) / 2
        cy = (self.base_ymin + self.base_ymax) / 2

        self.xmin = cx - largura / 2
        self.xmax = cx + largura / 2
        self.ymin = cy - altura / 2
        self.ymax = cy + altura / 2





