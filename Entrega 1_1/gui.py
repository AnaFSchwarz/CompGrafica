from tkinter import *
from ponto import Ponto
from reta import Reta
from wireframe import *

class App():
    def __init__(self):
        self.root = Tk()
        self.root.title("Sistema Gráfico Interativo 2D")
        self.root.geometry("1000x700")


        # Window
        self.canvas_width = 700
        self.canvas_height = 700
        self.canvas = Canvas(self.root, width=self.canvas_width, height= self.canvas_height, bg="white")
        self.canvas.pack(side="right", fill="both", expand=False)
        
        # Coluna de menu
        menu_frame = Frame(self.root, bg="#A29D9D", width=200)
        menu_frame.pack(side="left", fill="y")

        # Lista de seleção de objetos
        Label(menu_frame, text="Objetos:", width=20, bg="#808080", fg="white", font=("Arial", 10, "bold")).pack(pady=(20, 5))

        self.lista_objetos = Listbox(menu_frame, height=5, width=40, exportselection=False)
        self.lista_objetos.pack(padx=5)

        # Adicionar opções à lista
        # lista_objetos = ["Ponto", "Segmento de reta", "Wireframe"] 

        for item in ["Ponto", "Segmento de reta", "Wireframe"]:
            self.lista_objetos.insert(END, item)
        self.lista_objetos.bind("<<ListboxSelect>>", self.selecao_objeto)

        # Frame para os botões de movimentação
        movimento_frame = Frame(menu_frame, bg="#808080")
        movimento_frame.pack(pady=50)  # Espaço vertical

        btn_cima = Button(movimento_frame, text="CIMA", width=10, height=2)
        btn_cima.grid(row=0, column=1, padx=5, pady=5)

        btn_esquerda = Button(movimento_frame, text="ESQUERDA", width=10, height=2)
        btn_esquerda.grid(row=1, column=0, padx=5, pady=5)

        btn_direita = Button(movimento_frame, text="DIREITA", width=10, height=2)
        btn_direita.grid(row=1, column=2, padx=5, pady=5)

        btn_baixo = Button(movimento_frame, text="BAIXO", width=10, height=2)
        btn_baixo.grid(row=2, column=1, padx=5, pady=5)

        self.desenhar_eixo()

        self.run()

    def selecao_objeto(self, event):
        # Pega o índice selecionado
        idx = self.lista_objetos.curselection()
        if not idx:
            return  # nada selecionado
        nome = self.lista_objetos.get(idx)
        self.executar_objeto(nome)

    def executar_objeto(self, nome):
        if nome == "Ponto":
            self.desenhar_ponto()
        elif nome == "Segmento de reta":
            self.desenhar_reta()
        elif nome == "Wireframe":
            self.desenhar_wireframe()

    def desenhar_eixo(self):

        #Desenha eixo de coordenadas

        largura = int(self.canvas['width'])
        altura = int(self.canvas['height'])
        
        # Centro do canvas
        cx, cy = largura // 2, altura // 2
        
        # Eixo X (horizontal)
        self.canvas.create_line(0, cy, largura, cy, fill="gray", width=2, arrow=LAST)
        
        # Eixo Y (vertical)
        self.canvas.create_line(cx, 0, cx, altura, fill="gray", width=2, arrow=LAST)
        
        # Rótulos dos eixos
        self.canvas.create_text(largura - 10, cy - 10, text="X", fill="gray", font=("Arial", 10, "bold"))
        self.canvas.create_text(cx + 10, 10, text="Y", fill="gray", font=("Arial", 10, "bold"))
        
        # Marcas no eixo X
        for x in range(0, largura, 50):
            self.canvas.create_line(x, cy-5, x, cy+5, fill="gray")
            self.canvas.create_text(x, cy+15, text=str(x-cx), font=("Arial", 8))
        
        # Marcas no eixo Y
        for y in range(0, altura, 50):
            self.canvas.create_line(cx-5, y, cx+5, y, fill="gray")
            self.canvas.create_text(cx+20, y, text=str(cy-y), font=("Arial", 8))

    def run(self):
        """Inicia loop da aplicação"""
        self.root.mainloop()

    def desenhar_reta(self):
        retas = Reta(self.canvas, 4, 0 , 300, 200)
        self.desenhar_eixo()

    def desenhar_ponto(self):
        pontos = Ponto(self.canvas, 50, 50)
        self.desenhar_eixo()

    def desenhar_wireframe(self):
        pontos = [(150, 200), (200, 100), (250, 200), (200, 250)]
        wireframe = Wireframe(self.canvas, pontos)
        self.desenhar_eixo()




