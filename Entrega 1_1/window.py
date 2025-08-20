from tkinter import *
from tkinter import messagebox

class window():
    def __init__(self, xmin= -100, xmax=100, ymin= -100, ymax=100):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
    
    def set_tamx(self, tamx):
        if (tamx > 200) or (tamx < 2):
            messagebox.showerror("Erro de tamanho", "O valor deve estar entre 2 e 200.")
        tamx_i = self.get_tamx()
        var = (tamx - tamx_i)/2
        min = self.xmin - var
        max = self.xmax + var
        if min >= -100:
            self.xmin = min
        else:
            self.xmin = -100
            self.xmax = min + 100 + self.xmax
        
        if max <= 100:
            self.xmax = max        
        else:
            self.xmax = 100
            self.xmax = self.xmin - (max - 100)

            

    def get_tamx(self):
        tamx = self.xmax - self.xmin
        return tamx
    
    def get_tamy(self):
        tamy = self.ymax - self.ymin
        return tamy

    def move_window_direira(self):
        # mover sempre 5 "casas"
        # reduz os x e xmin como param de limite
        if (self.xmax + 5) >= 100:
           aux = (self.xmax + 5) - 100
           self.xmax += aux
           self.xmin += aux
        else:
            self.xmax += 5
            self.xmin += 5

    def move_window_esquerda(self):
        # aumento os x e xmax como param de limite
        if (self.xmin - 5) <= -100:
           aux = (self.xmin - 5) + 100
           self.xmax -= aux
           self.xmin -= aux
        else:
            self.xmax -= 5
            self.xmin -= 5

    def move_window_cima(self):
        # reduz os y e ymin como param de limite
        if (self.ymin - 5) <= -100:
           aux = (self.ymin - 5) + 100
           self.ymax -= aux
           self.ymin -= aux
        else:
            self.ymax -= 5
            self.ymin -= 5
        

    def move_window_baixo(self):
        # aumento os y e ymax como param de limite
        if (self.ymax + 5) >= 100:
           aux = (self.ymax + 5) - 100
           self.ymax += aux
           self.ymin += aux
        else:
            self.ymax += 5
            self.ymin += 5


"""
 messagebox.showinfo(self.root, "Partida abandonada. Você venceu!")

 """