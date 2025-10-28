from objeto import ObjetoGrafico
import math

# Variáveis para algoritmo de Cohen-Sutherland
INSIDE = 0
LEFT   = 1
RIGHT  = 2
BOTTOM = 4
TOP    = 8

class Reta(ObjetoGrafico):

    def desenhar(self, canvas, window, scn, viewport):
        aceito, (xc1, yc1, xc2, yc2) = self.clipping(self.pontos[0][0], self.pontos[0][1], self.pontos[1][0], self.pontos[1][1], window)
        (x1, y1) = self.rotacao_window(xc1, yc1)
        (x2, y2) = self.rotacao_window(xc2, yc2)

        # Se há parte visível dentro da window
        if aceito:
            xv1, yv1 = scn.world_to_scn_to_viewport(x1, y1, window, viewport)
            xv2, yv2 = scn.world_to_scn_to_viewport(x2, y2, window, viewport)
            canvas.create_line(xv1, yv1, xv2, yv2, fill=self.cor, width=2)

    def _compute_outcode(self, x, y, window):
        xmin, xmax, ymin, ymax = window.base_xmin, window.base_xmax, window.base_ymin, window.base_ymax
        code = INSIDE
        if x < xmin: code |= LEFT
        elif x > xmax: code |= RIGHT
        if y < ymin: code |= BOTTOM
        elif y > ymax: code |= TOP
        return code

    def clipping(self, x1, y1, x2, y2, window):

        xmin, xmax, ymin, ymax = window.base_xmin, window.base_xmax, window.base_ymin, window.base_ymax

        if self.tipo_clipping.get() == 1:
            # Algoritmo de Cohen–Sutherland 
            outcode1 = self._compute_outcode(x1, y1, window)
            outcode2 = self._compute_outcode(x2, y2, window)
            aceito = False

            while True:
                if outcode1 == 0 and outcode2 == 0:
                    aceito = True
                    break
                elif (outcode1 & outcode2) != 0:
                    break
                else:
                    if outcode1 != 0:
                        outcode_out = outcode1
                    else:
                        outcode_out = outcode2

                    if outcode_out & TOP:
                        x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                        y = ymax
                    elif outcode_out & BOTTOM:
                        x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                        y = ymin
                    elif outcode_out & RIGHT:
                        y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                        x = xmax
                    elif outcode_out & LEFT:
                        y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                        x = xmin

                    if outcode_out == outcode1:
                        x1, y1 = x, y
                        outcode1 = self._compute_outcode(x1, y1, window)
                    else:
                        x2, y2 = x, y
                        outcode2 = self._compute_outcode(x2, y2, window)

            return aceito, (x1, y1, x2, y2)
        
        else:
            # Algoritmo Liang–Barsky line clipping
            dx = x2 - x1
            dy = y2 - y1

            p = [-dx, dx, -dy, dy]
            q = [x1 - xmin, xmax - x1, y1 - ymin, ymax - y1]

            u1, u2 = 0.0, 1.0
            aceito = True

            for i in range(4):
                pk = p[i]
                qk = q[i]
                
                if pk == 0:
                    if qk < 0:
                        aceito = False
                        break
                else:
                    t = qk / pk
                    if pk < 0:
                        u1 = max(u1, t)
                    else:
                        u2 = min(u2, t)

            if u1 > u2:
                aceito = False

            if aceito:
                new_x1 = x1 + u1 * dx
                new_y1 = y1 + u1 * dy
                new_x2 = x1 + u2 * dx
                new_y2 = y1 + u2 * dy
                return True, (new_x1, new_y1, new_x2, new_y2)
            else:
                return False, (x1, y1, x2, y2)
