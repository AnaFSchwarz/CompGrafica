from objeto import ObjetoGrafico
import math

class Wireframe(ObjetoGrafico):

    def desenhar(self, canvas, window, scn, viewport):
        """
        Desenha o objeto no canvas.
        - Se 'pontos' for fornecido, usa esses pontos (ex: rotacionados).
        - Caso contrário, usa self.pontos.
        """
        #if pontos is None:
        pontos = self.pontos

        n = len(pontos)

        # ângulo da window em radianos
        theta = math.radians(window.angulo)
        cos_a = math.cos(theta)
        sin_a = math.sin(theta)

        def rot(x, y):
            xr = x * cos_a - y * sin_a
            yr = x * sin_a + y * cos_a
            return xr, yr

        for i in range(n):
            # aplica rotação on-the-fly
            x1, y1 = rot(*pontos[i])
            x2, y2 = rot(*pontos[(i+1) % n])  # conecta último com o primeiro

            xv1, yv1 = scn.world_to_scn_to_viewport(x1, y1, window, viewport)
            xv2, yv2 = scn.world_to_scn_to_viewport(x2, y2, window, viewport)

            canvas.create_line(xv1, yv1, xv2, yv2, fill=self.cor, width=2)

