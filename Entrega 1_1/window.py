from tkinter import *
from tkinter import messagebox

class window():
    def __init__(self, xmin=-350, xmax=350, ymin=-350, ymax= 50):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.tam_max = 700
        self.tam_min = 2
    
    def set_tam(self, tam):
        if (tam > self.tam_max) or (tam < self.tam_min):
            messagebox.showerror("Erro de tamanho", "O valor deve estar entre 2 e 700.")
        tam_i = self.get_tam()
        var = (tam - tam_i)/2

        min_x = self.xmin - var
        max_x = self.xmax + var
        if min_x >= -350:
            self.xmin = min_x
        else:
            self.xmin = -350
            self.xmax = min_x + 350 + self.xmax
        
        if max_x <= 350:
            self.xmax = max_x        
        else:
            self.xmax = 350
            self.xmax = self.xmin - (max_x - 350)

        min_y = self.ymin - var
        max_y = self.ymax + var
        if min_y >= -350:
            self.ymin = min_y
        else:
            self.ymin = -350
            self.ymax = min_y + 350 + self.ymax
        
        if max_y <= 350:
            self.ymax = max_y        
        else:
            self.ymax = 350
            self.ymax = self.ymin - (max_y - 350)

    
    def get_tam(self):
        tamx = self.xmax - self.xmin
        return tamx
    
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