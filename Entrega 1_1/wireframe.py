
from tkinter import *

class Wireframe():

    # Desenha polígono apenas com pontos e linhas

    def __init__(self, canva_desenho, lista_pontos):

        self.lista_pontos = lista_pontos
        
        canva_desenho.delete("all")

        raio_pontos = 2
        n = len(self.lista_pontos)

        for i in range(n):
            x1, y1 = self.lista_pontos[i]
            # Desenha o ponto
            canva_desenho.create_oval(
                x1 - raio_pontos, y1 - raio_pontos, x1 + raio_pontos, y1 + raio_pontos,
                fill="blue", tags="poligono"
            )

            # Pega o próximo ponto (cíclico, último liga ao primeiro)
            x2, y2 = self.lista_pontos[(i+1) % n]
            # Desenha a linha
            canva_desenho.create_line(
                x1, y1, x2, y2, fill="blue", width=2, tags="poligono"
            )