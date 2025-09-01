from objeto import ObjetoGrafico

class Ponto(ObjetoGrafico):

    def __init__(self, pontos, cor="#FF0000"):
        """
        pontos: lista de tuplas [(x,y), ...]
        cor: string hexadecimal ou nome de cor (Tkinter)
        """
        super().__init__(pontos, cor)

    def desenhar(self, canvas, window, viewport):
        xw, yw = self.pontos[0]
        xv, yv = viewport.world_to_viewport(xw, yw, window)
        raio = 2
        canvas.create_oval(xv-raio, yv-raio, xv+raio, yv+raio, fill=self.cor, outline=self.cor)
