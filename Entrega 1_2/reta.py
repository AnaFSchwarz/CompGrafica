from objeto import ObjetoGrafico

class Reta(ObjetoGrafico):
    def desenhar(self, canvas, window, viewport):
        (x1, y1), (x2, y2) = self.pontos
        xv1, yv1 = viewport.world_to_viewport(x1, y1, window)
        xv2, yv2 = viewport.world_to_viewport(x2, y2, window)
        canvas.create_line(xv1, yv1, xv2, yv2, fill=self.cor, width=2)

