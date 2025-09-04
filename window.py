from tkinter import *
from tkinter import messagebox

class Window():
    def __init__(self, xmin=-1, xmax=1, ymin=-1, ymax= 1):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
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
        fator = 1 - (fator_per / 100)  
        tam_f = fator * 698 + 2   # tamanho (2 a 700)

        cx = (self.xmin + self.xmax) / 2
        cy = (self.ymin + self.ymax) / 2

        half = tam_f / 2
        self.xmin, self.xmax = cx - half, cx + half
        self.ymin, self.ymax = cy - half, cy + half




