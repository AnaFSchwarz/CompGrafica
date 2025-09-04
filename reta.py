from objeto import ObjetoGrafico

class Reta(ObjetoGrafico):
    def desenhar(self, canvas, window, scn, viewport):
        #(x1, y1), (x2, y2) = self.pontos
        (x1, y1) = self.rotacao_window(*self.pontos[0])
        (x2, y2) = self.rotacao_window(*self.pontos[1])
        xv1, yv1 = scn.world_to_scn_to_viewport(x1, y1, window, viewport)
        xv2, yv2 = scn.world_to_scn_to_viewport(x2, y2, window, viewport)
        canvas.create_line(xv1, yv1, xv2, yv2, fill=self.cor, width=2)

