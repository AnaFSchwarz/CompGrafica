from objeto import ObjetoGrafico
import math
class Curva(ObjetoGrafico):

    def __init__(self, pontos, cor="#FF0000", window = None):
        super().__init__(pontos, cor, window)
        self.segmentos = []
        self.steps = 100
        print("debug")
        self.adicionar_curva(self.pontos)


    def desenhar(self, canvas, window, scn, viewport):
        print ("DEBUG VAI desenhar")
        pts = self.todos_pontos(self.steps)
        for i in range(len(pts)-1):
            x1,y1 = pts[i]
            x2,y2 = pts[i+1]
            canvas.create_line(x1,y1,x2,y2, fill=self.cor, width=2)
        print ("DEBUG desenhou curva")
        

        # usa o polígono recortado
        #pontos_clipados = self.clipping(window)

        #if not pontos_clipados:
        #    return  # nada para desenhar

    
    def adicionar_curva(self, pontos):
        print ("DEBUG VAI ADD")
        p0,p1,p2,p3 = pontos
        # Se já houver curvas, garantir G(0) (continuidade de posição)
        if self.segmentos and self.segmentos[-1][3] != p0:
            raise ValueError("Violação de G(0): p0 não coincide com o fim da curva anterior")
        self.segmentos.append((p0, p1, p2, p3))
        print ("DEBUG adicionou curvas")
        

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
        all_pts = []
        for idx, (p0,p1,p2,p3) in enumerate(self.segmentos):
            seg = self._pontos_bezier(p0,p1,p2,p3,steps)
            if idx > 0:
                seg = seg[1:]  # evita repetir o ponto inicial
            all_pts.extend(seg)
        return all_pts