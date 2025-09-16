from objeto import ObjetoGrafico
import math

class Wireframe(ObjetoGrafico):

    def desenhar(self, canvas, window, scn, viewport):
        # usa o polígono recortado
        pontos_clipados = self.clipping(window)

        if not pontos_clipados:
            return  # nada para desenhar

        n = len(pontos_clipados)
        for i in range(n):
            # aplica rotação on-the-fly
            x1, y1 = self.rotacao_window(*pontos_clipados[i])
            x2, y2 = self.rotacao_window(*pontos_clipados[(i+1) % n])  # conecta último com o primeiro

            xv1, yv1 = scn.world_to_scn_to_viewport(x1, y1, window, viewport)
            xv2, yv2 = scn.world_to_scn_to_viewport(x2, y2, window, viewport)

            canvas.create_line(xv1, yv1, xv2, yv2, fill=self.cor, width=2)

    def clipping(self, window):
        """
        Clipping poligonal usando Weiler-Atherton.
        Mantém self.pontos intacto.
        """
        xmin, xmax = window.base_xmin, window.base_xmax
        ymin, ymax = window.base_ymin, window.base_ymax

        # Copia os pontos originais
        subject_polygon = self.pontos[:]

        # Window é um retângulo -> usamos Sutherland–Hodgman (caso particular do Weiler-Atherton)
        def inside(p, edge):
            x, y = p
            if edge == "LEFT":   return x >= xmin
            if edge == "RIGHT":  return x <= xmax
            if edge == "BOTTOM": return y >= ymin
            if edge == "TOP":    return y <= ymax

        def intersect(p1, p2, edge):
            x1, y1 = p1
            x2, y2 = p2
            if x1 == x2 and y1 == y2:
                return p1

            if edge in ("LEFT", "RIGHT"):
                x_edge = xmin if edge == "LEFT" else xmax
                m = (y2 - y1) / (x2 - x1) if x2 != x1 else float("inf")
                y = m * (x_edge - x1) + y1
                return (x_edge, y)
            else:  # TOP ou BOTTOM
                y_edge = ymin if edge == "BOTTOM" else ymax
                m = (x2 - x1) / (y2 - y1) if y2 != y1 else float("inf")
                x = m * (y_edge - y1) + x1
                return (x, y_edge)

        def clip_polygon(subject_polygon, edge):
            output_list = []
            n = len(subject_polygon)
            for i in range(n):
                curr = subject_polygon[i]
                prev = subject_polygon[(i - 1) % n]

                if inside(curr, edge):
                    if not inside(prev, edge):
                        output_list.append(intersect(prev, curr, edge))
                    output_list.append(curr)
                elif inside(prev, edge):
                    output_list.append(intersect(prev, curr, edge))

            return output_list

        # Aplica contra cada lado da window
        clipped = subject_polygon
        for edge in ["LEFT", "RIGHT", "BOTTOM", "TOP"]:
            clipped = clip_polygon(clipped, edge)
            if not clipped:
                break

        return clipped

