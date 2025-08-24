from objeto import ObjetoGrafico

class Ponto(ObjetoGrafico):
    def desenhar(self, canvas, window, viewport):
        xw, yw = self.pontos[0]
        xv, yv = viewport.world_to_viewport(xw, yw, window)
        raio = 2
        canvas.create_oval(xv-raio, yv-raio, xv+raio, yv+raio, fill="red")
