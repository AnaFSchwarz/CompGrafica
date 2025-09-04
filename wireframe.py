from objeto import ObjetoGrafico
import math

class Wireframe(ObjetoGrafico):

    def desenhar(self, canvas, window, scn, viewport):

        n = len(self.pontos)

        for i in range(n):
            # aplica rotação on-the-fly
            x1, y1 = self.rotacao_window(*self.pontos[i])
            x2, y2 = self.rotacao_window(*self.pontos[(i+1) % n])  # conecta último com o primeiro

            xv1, yv1 = scn.world_to_scn_to_viewport(x1, y1, window, viewport)
            xv2, yv2 = scn.world_to_scn_to_viewport(x2, y2, window, viewport)

            canvas.create_line(xv1, yv1, xv2, yv2, fill=self.cor, width=2)

