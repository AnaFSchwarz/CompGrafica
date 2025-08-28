class Viewport:
    def __init__(self, xv_min=2, xv_max=700, yv_min=2, yv_max=700):
        self.xv_min = xv_min
        self.xv_max = xv_max
        self.yv_min = yv_min
        self.yv_max = yv_max

    def world_to_viewport(self, xw, yw, window):
        """Transforma coordenadas do mundo (window) em pixels (viewport)"""
        xv = self.xv_min + (xw - window.xmin) * (self.xv_max - self.xv_min) / (window.xmax - window.xmin)
        yv = self.yv_max - (yw - window.ymin) * (self.yv_max - self.yv_min) / (window.ymax - window.ymin)
        return xv, yv
