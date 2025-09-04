class Viewport:
    
    def __init__(self, xv_min=2, xv_max=700, yv_min=2, yv_max=700):
        self.xv_min = xv_min
        self.xv_max = xv_max
        self.yv_min = yv_min
        self.yv_max = yv_max

    def scn_to_viewport(self, xn, yn):
        """
        Transforma coordenadas no SCN (0 a 1) para coordenadas em pixels (viewport).
        Atenção: o eixo Y da tela cresce para baixo, então invertendo yn.
        """
        xv = self.xv_min + xn * (self.xv_max - self.xv_min)
        yv = self.yv_max - yn * (self.yv_max - self.yv_min)
        return xv, yv
