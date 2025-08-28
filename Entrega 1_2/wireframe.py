from objeto import ObjetoGrafico

class Wireframe(ObjetoGrafico):
    
    def desenhar(self, canvas, window, viewport):
        n = len(self.pontos)
        for i in range(n):
            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[(i+1) % n]  # conecta último com o primeiro

            xv1, yv1 = viewport.world_to_viewport(x1, y1, window)
            xv2, yv2 = viewport.world_to_viewport(x2, y2, window)

            canvas.create_line(xv1, yv1, xv2, yv2, fill="green", width=2)
