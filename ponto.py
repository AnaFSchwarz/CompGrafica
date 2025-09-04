from objeto import ObjetoGrafico

class Ponto(ObjetoGrafico):

    def __init__(self, pontos, cor="#FF0000", window = None):
        """
        pontos: lista de tuplas [(x,y), ...]
        cor: string hexadecimal ou nome de cor (Tkinter)
        """
        super().__init__(pontos, cor, window)

    def desenhar(self, canvas, window, scn, viewport):
        #xw, yw = self.pontos[0]
        xw, yw = self.rotacao_window(*self.pontos[0])
        xv, yv = scn.world_to_scn_to_viewport(xw, yw, window, viewport)
        raio = 2
        canvas.create_oval(xv-raio, yv-raio, xv+raio, yv+raio, fill=self.cor, outline=self.cor)
