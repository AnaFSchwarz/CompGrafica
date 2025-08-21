
from tkinter import *

class Ponto():

    def __init__(self, canva_desenho, x, y):

        # Limpar window
        canva_desenho.delete("all")
        r = 2
        canva_desenho.create_oval(x-r, y-r, x+r, y+r, fill="black")