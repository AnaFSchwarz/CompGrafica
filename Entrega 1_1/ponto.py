
from tkinter import *

class Ponto():

    def __init__(self, canva_desenho, x, y):

        # Limpar window
        canva_desenho.delete("all")
        # Define raio do ponto
        raio_pontos = 2
        # Desenha o ponto no espaço canva
        canva_desenho.create_oval(x-raio_pontos, y-raio_pontos, x+raio_pontos, y+raio_pontos, fill="black")