import numpy as np
from math import cos, sin, radians
from abc import ABC, abstractmethod
import math


class ObjetoGrafico3D(ABC):
    def __init__(self, pontos, cor, arestas, window, tipo_objeto = "3D", tipo_clipping = 1):
        self.pontos = [(x/100, y/100, z/100) for (x, y, z) in pontos]
        self.cor = cor
        self.tipo_clipping = tipo_clipping
        self.window = window
        self.tipo_objeto = tipo_objeto
        self.arestas = arestas

    def desenhar(self, canvas, window, scn, viewport):

        # projeta arestas para 2D
        proj = self.projetar_paralela_ortogonal()

        # recorta cada segmento projetado contra a window
        segmentos_clipados = self.clipping(window, proj)

        if not segmentos_clipados:
            return  # nada para desenhar

        for (x1, y1), (x2, y2) in segmentos_clipados:
            # aplica rotação da janela (on-the-fly) nos pontos 2D
            xr1, yr1 = self.rotacao_window(x1, y1)
            xr2, yr2 = self.rotacao_window(x2, y2)

            # converte para viewport/scn e desenha
            xv1, yv1 = scn.world_to_scn_to_viewport(xr1, yr1, window, viewport)
            xv2, yv2 = scn.world_to_scn_to_viewport(xr2, yr2, window, viewport)
            canvas.create_line(xv1, yv1, xv2, yv2, fill=self.cor, width=2)

    def clipping(self, window, segments=None):
        """
        Clipping de segmentos 2D usando Cohen–Sutherland.
        - Se 'segments' for None, usa as arestas projetadas.
        - Retorna lista de segmentos já recortados: [ ((x1,y1),(x2,y2)), ... ]
        """
        if segments is None:
            segments = self.projetar_paralela_ortogonal()

        xmin, xmax = window.base_xmin, window.base_xmax
        ymin, ymax = window.base_ymin, window.base_ymax

        # Códigos de região (bitwise)
        INSIDE = 0  # 0000
        LEFT   = 1  # 0001
        RIGHT  = 2  # 0010
        BOTTOM = 4  # 0100
        TOP    = 8  # 1000

        def _region_code(x, y):
            code = INSIDE
            if x < xmin:   code |= LEFT
            elif x > xmax: code |= RIGHT
            if y < ymin:   code |= BOTTOM
            elif y > ymax: code |= TOP
            return code

        def _compute_intersection(x1, y1, x2, y2, edge_flag):
            # calcula interseção entre segmento (x1,y1)-(x2,y2) e a aresta indicada por edge_flag
            dx = x2 - x1
            dy = y2 - y1
            if edge_flag & LEFT:
                x = xmin
                if dx == 0:
                    return None
                t = (xmin - x1) / dx
                y = y1 + t * dy
                return x, y
            if edge_flag & RIGHT:
                x = xmax
                if dx == 0:
                    return None
                t = (xmax - x1) / dx
                y = y1 + t * dy
                return x, y
            if edge_flag & BOTTOM:
                y = ymin
                if dy == 0:
                    return None
                t = (ymin - y1) / dy
                x = x1 + t * dx
                return x, y
            if edge_flag & TOP:
                y = ymax
                if dy == 0:
                    return None
                t = (ymax - y1) / dy
                x = x1 + t * dx
                return x, y
            return None

        clipped_segments = []

        for (p1, p2) in segments:
            x1, y1 = p1
            x2, y2 = p2

            rc1 = _region_code(x1, y1)
            rc2 = _region_code(x2, y2)

            accept = False

            while True:
                # Trivial aceitação
                if (rc1 | rc2) == 0:
                    accept = True
                    break
                # Trivial rejeição
                if (rc1 & rc2) != 0:
                    accept = False
                    break
                # caso contrário, calcula interseção
                # escolhe um ponto fora da janela
                out_code = rc1 if rc1 != 0 else rc2
                inter = _compute_intersection(x1, y1, x2, y2, out_code)
                if inter is None:
                    # segmento paralelo e fora; rejeita
                    accept = False
                    break
                xi, yi = inter

                # substitui o ponto fora pelo ponto de interseção e recomputa código
                if out_code == rc1:
                    x1, y1 = xi, yi
                    rc1 = _region_code(x1, y1)
                else:
                    x2, y2 = xi, yi
                    rc2 = _region_code(x2, y2)

            if accept:
                # garante tipos float e adiciona
                clipped_segments.append(((float(x1), float(y1)), (float(x2), float(y2))))

        return clipped_segments

    def _aplicar_transformacao(self, matriz):
        novos_pontos = []
        for (x,y,z) in self.pontos:
            ponto_h = np.array([x,y,z,1])
            ponto_trans = (matriz @ ponto_h)
            novos_pontos.append((ponto_trans[0], ponto_trans[1], ponto_trans[2]))
        self.pontos = novos_pontos

    def transladar(self, dx, dy, dz=0):
        matriz = np.array([
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ])
        self._aplicar_transformacao(matriz)

    def escalonar(self, sx, sy, sz=0):
        matriz = np.array([
            [sx, 0,  0,  0],
            [0,  sy, 0,  0],
            [0,  0,  sz, 0],
            [0,  0,  0,  1]
        ])
        self._aplicar_transformacao(matriz)

    def centro(self):
        xs = [p[0] for p in self.pontos]
        ys = [p[1] for p in self.pontos]
        zs = [p[2] for p in self.pontos]
        return sum(xs)/len(xs), sum(ys)/len(ys), sum(zs)/len(zs)

    def rotacionar(self, angulo, cx, cy, cz):

        a = radians(angulo)

        # Matrizes de rotação para cada eixo
        Rx = np.array([
            [1, 0,      0,       0],
            [0, cos(a), -sin(a), 0],
            [0, sin(a), cos(a),  0],
            [0, 0,      0,       1]
        ], dtype=float)

        Ry = np.array([
            [cos(a),  0, sin(a), 0],
            [0,        1, 0,       0],
            [-sin(a), 0, cos(a), 0],
            [0,        0, 0,       1]
        ], dtype=float)

        Rz = np.array([
            [cos(a), -sin(a), 0, 0],
            [sin(a),  cos(a), 0, 0],
            [0,        0,       1, 0],
            [0,        0,       0, 1]
        ], dtype=float)

        # Matriz de translação para mover para origem e retornar
        T_origem = np.array([
            [1, 0, 0, -cx],
            [0, 1, 0, -cy],
            [0, 0, 1, -cz],
            [0, 0, 0, 1]
        ], dtype=float)

        T_volta = np.array([
            [1, 0, 0, cx],
            [0, 1, 0, cy],
            [0, 0, 1, cz],
            [0, 0, 0, 1]
        ], dtype=float)

        # Matriz composta: aplica X depois Y depois Z
        matriz_total = T_volta @ (Rz @ (Ry @ (Rx @ T_origem)))

        # aplica transformação
        self._aplicar_transformacao(matriz_total)


    def projetar_paralela_ortogonal(self):
        """
        Como o VPN deve ser (0,0,1), projetamos 'descartando z'
        Retorna lista de segmentos 2D projetados
        """
        proj = []
        for i, j in self.arestas:
            p1, p2 = self.pontos[i], self.pontos[j]
            proj.append(((p1[0], p1[1]), (p2[0], p2[1])))
        return proj
    
    def rotacao_window(self,x, y):

        tetha = math.radians(self.window.angulo)
        cos_a = math.cos(tetha)
        sin_a = math.sin(tetha)

        xr = x * cos_a - y * sin_a
        yr = x * sin_a + y * cos_a
        return xr, yr