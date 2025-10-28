
class SCN:
    def __init__(self):
        # O SCN é sempre fixo: [0,1] em x e y.
        self.xn_min = 0.0
        self.xn_max = 1.0
        self.yn_min = 0.0
        self.yn_max = 1.0

    def world_to_scn_to_viewport(self, xw, yw, window, viewport):
        """
        Converte coordenadas do mundo (WC) para SCN.
        - xw, yw: coordenadas no mundo (window coordinates)
        - window: instância de Window com limites xmin, xmax, ymin, ymax
        Retorna (xn, yn) no intervalo [0,1].
        """
        xn = (xw - window.xmin) / (window.xmax - window.xmin)
        yn = (yw - window.ymin) / (window.ymax - window.ymin)

        return viewport.scn_to_viewport(xn,yn)

    def scn_to_world(self, xn, yn, window):
        """
        Converte coordenadas do SCN de volta para WC.
        - xn, yn: coordenadas normalizadas [0,1]
        - window: instância de Window
        """
        xw = window.xmin + xn * (window.xmax - window.xmin)
        yw = window.ymin + yn * (window.ymax - window.ymin)
        return xw, yw
