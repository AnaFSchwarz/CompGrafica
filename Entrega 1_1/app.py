from tkinter import *
from window import Window
from viewport import Viewport
from ponto import Ponto
from reta import Reta
from wireframe import Wireframe
from tkinter import simpledialog

class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Sistema Gráfico Interativo 2D")
        self.root.geometry("1000x700")

        # Canvas
        self.canvas_width = 700
        self.canvas_height = 700
        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side="right", fill="both", expand=False)

        # Window e Viewport
        self.window = Window()
        self.viewport = Viewport(0, self.canvas_width, 0, self.canvas_height)

        # Display file
        self.display_file = []

        # Menu lateral
        self._criar_menu()

        self.run()

    def _criar_menu(self):
        menu_frame = Frame(self.root, bg="#A29D9D", width=200)
        menu_frame.pack(side="left", fill="y")
        
        self.desenhar_eixos()

         # frame selcionar objetos
        Label(menu_frame, text="Objetos:", width=20, bg="#808080", fg="white", font=("Arial", 10, "bold")).pack(pady=(20, 5))

        self.lista_objetos = Listbox(menu_frame, height=5, width=40, exportselection=False)
        self.lista_objetos.pack(padx=5)
        for item in ["Ponto", "Reta", "Wireframe", ">>Limpar Tela<<"]:
            self.lista_objetos.insert(END, item)
        self.lista_objetos.bind("<<ListboxSelect>>", self.selecao_objeto)


         # frame botões de movimento
        movimento_frame = Frame(menu_frame, bg="#808080")
        movimento_frame.pack(pady=50)

        btn_cima = Button(movimento_frame, text="CIMA", width=10, height=2, command=lambda: self.mover_window(0, self.window.get_tam()/8))
        btn_cima.grid(row=0, column=1, padx=5, pady=5)

        btn_esquerda = Button(movimento_frame, text="ESQUERDA", width=10, height=2, command=lambda: self.mover_window(-self.window.get_tam()/8, 0))
        btn_esquerda.grid(row=1, column=0, padx=(2,5), pady=5)

        btn_centralizar = Button(movimento_frame, text="CENTRALIZAR", width=10, height=2, command= lambda: self.centralizar_window())
        btn_centralizar.grid(row=1, column=1, padx=(2,5), pady=5)

        btn_direita = Button(movimento_frame, text="DIREITA", width=10, height=2, command=lambda: self.mover_window(self.window.get_tam()/8, 0))
        btn_direita.grid(row=1, column=2, padx=(2,5), pady=5)

        btn_baixo = Button(movimento_frame, text="BAIXO", width=10, height=2, command=lambda: self.mover_window(0, -self.window.get_tam()/8))
        btn_baixo.grid(row=2, column=1, padx=5, pady=5)

        # frame zoom
        zoom_frame = Frame(menu_frame, bg="#808080", pady=5)
        zoom_frame.pack(pady=5, padx = 15)  # Frame para agrupar os widgets na mesma linha

        Label(zoom_frame, text="Zoom(%): ", bg="#808080", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        self.zoom_entry = Entry(zoom_frame, width=5)
        self.zoom_entry.insert(0, "0")
        self.zoom_entry.grid(row=0, column=1, padx=0)
        btn_zoom = Button(zoom_frame, text="Aplicar Zoom", command=self.aplicar_zoom)
        btn_zoom.grid(row=0, column=2, padx=50) 

    def mover_window(self, dx, dy):
        """Movimenta a window e redesenha"""
        self.window.mover(dx, dy)   # supondo que exista função mover na sua classe Window
        self.redesenhar()
    
    def centralizar_window(self):
        """Centralisa a window e redesenha"""
        self.window.centralizar()   # supondo que exista função mover na sua classe Window
        self.redesenhar()

    def aplicar_zoom(self):
        """Aplica o zoom com o fator digitado"""
        try:
            fator = float(self.zoom_entry.get())
            self.window.zoom(fator)
            self.redesenhar()
        except ValueError:
            print("Digite um número válido para o zoom")

    def selecao_objeto(self, event):
        idx = self.lista_objetos.curselection()
        if not idx: return
        nome = self.lista_objetos.get(idx)
        self.executar_objeto(nome)

    def executar_objeto(self, nome):
        if nome == "Ponto":
            x = simpledialog.askfloat("Coordenada X", "Digite X do ponto:")
            y = simpledialog.askfloat("Coordenada Y", "Digite Y do ponto:")
            if x is not None and y is not None:
                self.display_file.append(Ponto([(x, y)]))
        elif nome == "Reta":
            x1 = simpledialog.askfloat("Reta", "Digite X do ponto inicial:")
            y1 = simpledialog.askfloat("Reta", "Digite Y do ponto inicial:")
            x2 = simpledialog.askfloat("Reta", "Digite X do ponto final:")
            y2 = simpledialog.askfloat("Reta", "Digite Y do ponto final:")
            if None not in (x1, y1, x2, y2):
                self.display_file.append(Reta([(x1, y1), (x2, y2)]))
        elif nome == "Wireframe":
            pontos = []
            n = simpledialog.askinteger("Wireframe", "Quantos pontos deseja inserir?")
            if n is not None:
                for i in range(n):
                    x = simpledialog.askfloat(f"Ponto {i+1}", f"Digite X do ponto {i+1}:")
                    y = simpledialog.askfloat(f"Ponto {i+1}", f"Digite Y do ponto {i+1}:")
                    if x is None or y is None:
                        return
                    pontos.append((x, y))
                self.display_file.append(Wireframe(pontos))
        elif nome == ">>Limpar Tela<<":
            self.display_file.clear()

        self.redesenhar()

    def redesenhar(self):
        self.canvas.delete("all")
        self.desenhar_eixos()
        # self.window.desenha_eixos(self.canvas, self.viewport)
        for obj in self.display_file:
            obj.desenhar(self.canvas, self.window, self.viewport)

    def desenhar_eixos(self):
        xv1, yv1 = self.viewport.world_to_viewport(0, -350, self.window)  # ponto inferior
        xv2, yv2 = self.viewport.world_to_viewport(0, 350, self.window)   # ponto superior
        self.canvas.create_line(xv1, yv1, xv2, yv2, fill="gray", width=2,arrow='last',)

        # Eixo X (horizontal)
        xv1, yv1 = self.viewport.world_to_viewport(-350, 0, self.window)  # ponto esquerdo
        xv2, yv2 = self.viewport.world_to_viewport(350, 0, self.window)   # ponto direito
        self.canvas.create_line(xv1, yv1, xv2, yv2, fill="gray", width=2, arrow='last',)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    App()


