from objeto import ObjetoGrafico

# Variáveis para algoritmo de Cohen-Sutherland
INSIDE = 0
LEFT   = 1
RIGHT  = 2
BOTTOM = 4
TOP    = 8

class Reta(ObjetoGrafico):

    def desenhar(self, canvas, window, scn, viewport):
        (x1, y1) = self.rotacao_window(*self.pontos[0])
        (x2, y2) = self.rotacao_window(*self.pontos[1])

        aceito, (xc1, yc1, xc2, yc2) = self.clipping((x1, y1, x2, y2), window)

        # Se há parte visível dentro da window
        if aceito:
            print("DEBUG pontos originais da reta", self.pontos)
            print("DEBUG ACEITO pontos cutting", xc1, yc1, xc2, yc2)
            xv1, yv1 = scn.world_to_scn_to_viewport(xc1, yc1, window, viewport)
            xv2, yv2 = scn.world_to_scn_to_viewport(xc2, yc2, window, viewport)
            print("DEBUG ACEITO pontos scn", xv1, yv1, xv2, yv2)
            canvas.create_line(xv1, yv1, xv2, yv2, fill=self.cor, width=2)

        # Desenha as partes fora em cinza (se existirem)
        # Trecho 1: ponto inicial até o ponto recortado
        if (x1, y1) != (xc1, yc1) and 0==1:
            print("DEBUG (x1, y1) != (xc1, yc1) ", aceito)
            xv1, yv1 = scn.world_to_scn_to_viewport(x1, y1, window, viewport)
            xv2, yv2 = scn.world_to_scn_to_viewport(xc1, yc1, window, viewport)
            #self.cor = "light gray"
            canvas.create_line(xv1, yv1, xv2, yv2, fill="light gray", width=2)

        # Trecho 2: ponto final até o ponto recortado
        if (x2, y2) != (xc2, yc2) and 0==1:
            print("DEBUG (x2, y2) != (xc2, yc2) ", aceito)
            xv1, yv1 = scn.world_to_scn_to_viewport(x2, y2, window, viewport)
            xv2, yv2 = scn.world_to_scn_to_viewport(xc2, yc2, window, viewport)
            #self.cor = "light gray"
            canvas.create_line(xv1, yv1, xv2, yv2, fill="light gray", width=2)

    def _compute_outcode(self, x, y, window):
        xmin, xmax, ymin, ymax = window.xmin, window.xmax, window.ymin, window.ymax
        code = INSIDE
        if x < xmin: code |= LEFT
        elif x > xmax: code |= RIGHT
        if y < ymin: code |= BOTTOM
        elif y > ymax: code |= TOP
        return code

    def clipping(self, pontos, window):
        """ Algoritmo de Cohen–Sutherland """
        x1, y1, x2, y2 = pontos
        xmin, xmax, ymin, ymax = window.xmin, window.xmax, window.ymin, window.ymax

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
