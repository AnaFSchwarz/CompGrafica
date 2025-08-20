from tkinter import *

class App():
    def __init__(self):
        self.root = Tk()
        self.root.title("Sistema Gráfico Interativo 2D")

        self.canvas_width = width
        self.canvas_height = height
        self.canvas = Tk.Canvas(self.root, width=width, height=height, bg="white")
        self.canvas.pack(fill=Tk.BOTH, expand=True)
        
        menu_frame = Tk.Frame(self.root, bg="#808080", width=180)
        menu_frame.pack(side="left", fill="y")

        lista_objetos = ["Ponto", "Segmento de reta", "Wireframe"]

    def run(self):
        """Inicia loop da aplicação"""
        self.root.mainloop()
