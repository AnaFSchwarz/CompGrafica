import numpy as np
from math import cos, sin, radians
from abc import ABC, abstractmethod


class ObjetoGrafico3D(ABC):
    def __init__(self, pontos=None, cor="#00FF00", arestas=None, window=None, tipo_objeto="3D", tipo_clipping=1):
        """
        Para objetos que usam pontos/arestas (pontos é lista de (x,y,z) já em unidades naturais).
        Para superfícies, sobrescreva este comportamento.
        """
        self.pontos = []
        if pontos:
            # mantemos a convenção do seu código original (divisão por 100 se necessário fora)
            self.pontos = [(float(x), float(y), float(z)) for (x, y, z) in pontos]
        self.cor = cor
        self.tipo_clipping = tipo_clipping
        self.window = window
        self.tipo_objeto = tipo_objeto
        self.arestas = arestas or []

    def desenhar(self, canvas, largura, altura, cor=None):
        pass

    def _aplicar_transformacao(self, matriz):
        """
        Aplica transformação homogênea a self.pontos — sobrescrever em subclasses que armazenam
        pontos em outra estrutura (por exemplo superfícies 4x4).
        """
        novos_pontos = []
        for (x, y, z) in self.pontos:
            ponto_h = np.array([x, y, z, 1.0])
            ponto_trans = (matriz @ ponto_h)
            novos_pontos.append((float(ponto_trans[0]), float(ponto_trans[1]), float(ponto_trans[2])))
        self.pontos = novos_pontos

    def transladar(self, dx, dy, dz=0):
        matriz = np.array([
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ], dtype=float)
        self._aplicar_transformacao(matriz)

    def escalonar(self, sx, sy, sz=1):
        matriz = np.array([
            [sx, 0,  0,  0],
            [0,  sy, 0,  0],
            [0,  0,  sz, 0],
            [0,  0,  0,  1]
        ], dtype=float)
        self._aplicar_transformacao(matriz)

    def centro(self):
        if not self.pontos:
            return 0, 0, 0
        xs = [p[0] for p in self.pontos]
        ys = [p[1] for p in self.pontos]
        zs = [p[2] for p in self.pontos]
        return sum(xs) / len(xs), sum(ys) / len(ys), sum(zs) / len(zs)
    
    def rotacionar(self, angulo, cx, cy, cz):
        """
        Aplica rotações sucessivas em torno dos eixos X, Y e Z, 
        em torno de um único ponto (centro).
        
        Parâmetros:
        angulo_x, angulo_y, angulo_z : float
            ângulos de rotação em graus (padrão = 0)
        centro : tuple (cx, cy, cz)
            ponto fixo da rotação; se None, usa o centro geométrico do objeto
        """
        angulo_x = angulo
        angulo_y = angulo 
        angulo_z=  angulo

        # converte graus para radianos
        ax = radians(angulo_x)
        ay = radians(angulo_y)
        az = radians(angulo_z)

        # Matrizes de rotação para cada eixo
        Rx = np.array([
            [1, 0,      0,       0],
            [0, cos(ax), -sin(ax), 0],
            [0, sin(ax), cos(ax),  0],
            [0, 0,      0,       1]
        ], dtype=float)

        Ry = np.array([
            [cos(ay),  0, sin(ay), 0],
            [0,        1, 0,       0],
            [-sin(ay), 0, cos(ay), 0],
            [0,        0, 0,       1]
        ], dtype=float)

        Rz = np.array([
            [cos(az), -sin(az), 0, 0],
            [sin(az),  cos(az), 0, 0],
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

    # -----------------------------------------------------
    # ROTAÇÕES AGORA ACEITAM PARÂMETRO (cx, cy, cz)
    # -----------------------------------------------------
    def rotacionar_x(self, angulo, centro=None):
        cx, cy, cz = centro if centro else self.centro()
        a = radians(angulo)

        # transladar para origem, rotacionar, voltar
        trans_origem = np.array([
            [1, 0, 0, -cx],
            [0, 1, 0, -cy],
            [0, 0, 1, -cz],
            [0, 0, 0, 1]
        ], dtype=float)

        matriz_rot = np.array([
            [1, 0,      0,       0],
            [0, cos(a), -sin(a), 0],
            [0, sin(a), cos(a),  0],
            [0, 0,      0,       1]
        ], dtype=float)

        trans_volta = np.array([
            [1, 0, 0, cx],
            [0, 1, 0, cy],
            [0, 0, 1, cz],
            [0, 0, 0, 1]
        ], dtype=float)

        matriz_total = trans_volta @ matriz_rot @ trans_origem
        self._aplicar_transformacao(matriz_total)

    def rotacionar_y(self, angulo, centro=None):
        cx, cy, cz = centro if centro else self.centro()
        a = radians(angulo)
        trans_origem = np.array([
            [1, 0, 0, -cx],
            [0, 1, 0, -cy],
            [0, 0, 1, -cz],
            [0, 0, 0, 1]
        ], dtype=float)

        matriz_rot = np.array([
            [cos(a),  0, sin(a), 0],
            [0,       1, 0,      0],
            [-sin(a), 0, cos(a), 0],
            [0,       0, 0,      1]
        ], dtype=float)

        trans_volta = np.array([
            [1, 0, 0, cx],
            [0, 1, 0, cy],
            [0, 0, 1, cz],
            [0, 0, 0, 1]
        ], dtype=float)

        matriz_total = trans_volta @ matriz_rot @ trans_origem
        self._aplicar_transformacao(matriz_total)

    def rotacionar_z(self, angulo, centro=None):
        cx, cy, cz = centro if centro else self.centro()
        a = radians(angulo)
        trans_origem = np.array([
            [1, 0, 0, -cx],
            [0, 1, 0, -cy],
            [0, 0, 1, -cz],
            [0, 0, 0, 1]
        ], dtype=float)

        matriz_rot = np.array([
            [cos(a), -sin(a), 0, 0],
            [sin(a), cos(a),  0, 0],
            [0,      0,       1, 0],
            [0,      0,       0, 1]
        ], dtype=float)

        trans_volta = np.array([
            [1, 0, 0, cx],
            [0, 1, 0, cy],
            [0, 0, 1, cz],
            [0, 0, 0, 1]
        ], dtype=float)

        matriz_total = trans_volta @ matriz_rot @ trans_origem
        self._aplicar_transformacao(matriz_total)

    def projetar_paralela_ortogonal(self):
        """
        Para objetos com pontos/arestas (linhas). Para superfícies, sobrescrever.
        Retorna lista de segmentos 2D projetados [ ((x1,y1),(x2,y2)), ... ]
        """
        proj = []
        for i, j in (self.arestas or []):
            p1, p2 = self.pontos[i], self.pontos[j]
            proj.append(((p1[0], p1[1]), (p2[0], p2[1])))
        return proj


# ---------------------- CLASSE PARA SUPERFÍCIES BICÚBICAS DE BÉZIER ----------------------
class SuperficieBezier3D(ObjetoGrafico3D):
    def __init__(self, patches=None, cor="#00FF00", window=None, tipo_clipping=1):
        """
        patches: lista de patches; cada patch é um array shape (4,4,3) com coordenadas (x,y,z)
        Para conveniência, há também método factory from_control_points(list16) para criar um patch.
        """
        super().__init__(pontos=None, cor=cor, arestas=None, window=window, tipo_objeto="Surface3D", tipo_clipping=tipo_clipping)
        self.patches = patches or []  # cada patch é np.array((4,4,3), dtype=float)

    @classmethod
    def from_control_points(cls, cp16, cor="#00FF00", window=None):
        """
        cp16: lista de 16 tuplas (x,y,z) no *ordem row-major* para formar a matriz 4x4.
        Ordem esperada: linhas de v para u, ou seja:
        [ (u0v0), (u0v1), (u0v2), (u0v3),
          (u1v0), ... ]
        Retorna uma SuperficieBezier3D com um único patch.
        """
        if len(cp16) != 16:
            raise ValueError("Esperados 16 pontos de controle por patch")
        arr = np.array(cp16, dtype=float).reshape((4, 4, 3))
        return cls(patches=[arr], cor=cor, window=window)

    def _aplicar_transformacao(self, matriz):
        """
        Aplica matriz homogênea aos pontos de todos os patches.
        """
        novos_patches = []
        for patch in self.patches:
            # patch shape (4,4,3)
            pts = patch.reshape((-1, 3))
            pts_h = np.hstack([pts, np.ones((pts.shape[0], 1), dtype=float)])  # Nx4
            pts_t = (matriz @ pts_h.T).T  # Nx4
            pts3 = pts_t[:, :3].reshape((4, 4, 3))
            novos_patches.append(pts3)
        self.patches = novos_patches

    # ----------------- Blending (Bernstein) para Bézier bicúbico -----------------
    @staticmethod
    def bernstein_basis_3(t):
        """
        Retorna vetor [B0, B1, B2, B3] para t (bernstein cúbico)
        B0 = (1-t)^3
        B1 = 3t(1-t)^2
        B2 = 3t^2(1-t)
        B3 = t^3
        """
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        return np.array([mt3, 3 * t * mt2, 3 * t2 * mt, t3], dtype=float)

    def avaliar_patch(self, patch, u, v):
        """
        Avalia o patch (4x4x3) no parâmetro (u,v), retornando ponto 3D.
        Usa formula S(u,v) = U^T * G * V, implementada via blending: sum_{i,j} B_i(u)*B_j(v)*P_ij
        """
        Bu = self.bernstein_basis_3(u)  # (4,)
        Bv = self.bernstein_basis_3(v)  # (4,)
        # combinação tensorial:
        ponto = np.zeros(3, dtype=float)
        for i in range(4):
            for j in range(4):
                coeff = Bu[i] * Bv[j]
                ponto += coeff * patch[i, j, :]
        return tuple(ponto.tolist())

    def gerar_malha_parametrica(self, res_u=10, res_v=10):
        """
        Gera uma malha de pontos e segmentos (arestas) amostrando cada patch.
        Retorna (vertices, segmentos) onde:
         - vertices: lista de (x,y,z)
         - segmentos: lista de (i,j) índices em vertices conectando linhas na malha (u e v)
        res_u/res_v = número de amostras por direção (>=2)
        """
        vertices = []
        segmentos = []
        for patch_idx, patch in enumerate(self.patches):
            # para cada patch, cria grid de (res_u x res_v)
            base_index = len(vertices)
            grid = [[None for _ in range(res_v)] for __ in range(res_u)]
            for iu in range(res_u):
                u = iu / (res_u - 1)
                for iv in range(res_v):
                    v = iv / (res_v - 1)
                    p = self.avaliar_patch(patch, u, v)
                    vertices.append(p)
                    grid[iu][iv] = base_index + iu * res_v + iv
            # criar segmentos entre vizinhos horizontais e verticais
            for iu in range(res_u):
                for iv in range(res_v):
                    idx = grid[iu][iv]
                    if iu + 1 < res_u:
                        segmentos.append((idx, grid[iu + 1][iv]))
                    if iv + 1 < res_v:
                        segmentos.append((idx, grid[iu][iv + 1]))
        return vertices, segmentos

    def projetar_paralela_ortogonal(self, res_u=12, res_v=12):
        """
        Projeta a superfície amostrada para segmento 2D (descarta z) e retorna lista de segmentos 2D.
        """
        verts3, segs = self.gerar_malha_parametrica(res_u=res_u, res_v=res_v)
        proj = []
        for (i, j) in segs:
            p1 = verts3[i]
            p2 = verts3[j]
            proj.append(((p1[0], p1[1]), (p2[0], p2[1])))
        return proj

    # utilidade: retorna matrizes Gx, Gy, Gz para um patch (forma clássica para S(u,v)=U^T * M * G * M^T * V)
    def geometry_matrices(self, patch):
        """
        Retorna tupla (Gx, Gy, Gz) cada uma 4x4 contendo coordenadas X,Y,Z dos pontos de controle.
        """
        Gx = patch[:, :, 0].copy()
        Gy = patch[:, :, 1].copy()
        Gz = patch[:, :, 2].copy()
        return Gx, Gy, Gz

    # conveniência: adicione novo patch a partir de 16 pontos
    def adicionar_patch_de_pontos(self, cp16):
        if len(cp16) != 16:
            raise ValueError("Esperados 16 pontos de controle por patch")
        arr = np.array(cp16, dtype=float).reshape((4, 4, 3))
        self.patches.append(arr)

