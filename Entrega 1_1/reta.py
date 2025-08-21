
from tkinter import *

class Reta():

    def __init__(self, canva_desenho, lista_pontos):

        self.lista_pontos = lista_pontos
        
        canva_desenho.delete("all")

        x1, y1 = self.lista_pontos[0]
        x2, y2 = self.lista_pontos[1]
            # Desenha reta
        canva_desenho.create_line(x1, y1, x2, y2, fill="black", width=2)