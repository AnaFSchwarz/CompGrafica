from objeto import ObjetoGrafico
import math
class Curva(ObjetoGrafico):

    def __init__(self, pontos, cor="#FF0000", window = None):
        super().__init__(pontos, cor, window)
        self.tipo_objeto = "Curva"
        self.segmentos = []
        self.steps = 100

    def desenhar(self, canvas, window, scn, viewport):

        if len(self.pontos) == 4:
            self.segmentos = []
            self.adicionar_curva(self.pontos)

        # Altera self.pontos
        self.todos_pontos(self.steps)

        # usa o polígono recortado
        pontos_clipados = self.clipping(window)

        if not pontos_clipados:
            return  # nada para desenhar
   
        for i in range(len(pontos_clipados)-1):
             # aplica rotação on-the-fly
            xr1, yr1 = self.rotacao_window(*pontos_clipados[i])
            xr2, yr2 = self.rotacao_window(*pontos_clipados[(i+1)])  # conecta último com o primeiro

            xv1, yv1 = scn.world_to_scn_to_viewport(xr1, yr1, window, viewport)
            xv2, yv2 = scn.world_to_scn_to_viewport(xr2, yr2, window, viewport)
            canvas.create_line(xv1,yv1,xv2,yv2, fill=self.cor, width=2)

    def adicionar_curva(self, pontos):
        p0,p1,p2,p3 = pontos
        # Se já houver curvas, garantir G(0) (continuidade de posição)
        if self.segmentos and self.segmentos[-1][3] != p0:
            raise ValueError("Violação de G(0): p0 não coincide com o fim da curva anterior")
        self.segmentos.append([p0, p1, p2, p3])

        

    def _pontos_bezier(self, p0, p1, p2, p3, steps=50):
        pts = []
        for i in range(steps+1):
            t = i/steps
            x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
            y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
            pts.append((x,y))
        return pts

    def todos_pontos(self, steps=50):
        """Gera os pontos da curva composta como uma lista única."""
        if steps is None:
            steps = self.steps
        all_pts = []
        for idx, (p0, p1, p2, p3) in enumerate(self.segmentos):
            seg = self._pontos_bezier(p0, p1, p2, p3, steps)
            if idx > 0:
                seg = seg[1:]  # evita duplicar ponto inicial
            all_pts.extend(seg)
        #return all_pts
        self.pontos = all_pts
        #return all_pts
    
    def clipping (self, window):
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