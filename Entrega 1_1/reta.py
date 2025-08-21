
from tkinter import *

class Reta():

    def __init__(self, canva_desenho, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        canva_desenho.delete("all")
        canva_desenho.create_line(self.x1, self.y1, self.x2, self.y2, fill="black", width=2)