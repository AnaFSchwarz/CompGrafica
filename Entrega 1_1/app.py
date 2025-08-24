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
        self.lista_obj = []

        # Menu lateral
        self._criar_menu()

        self.run()

    def _criar_menu(self):
        menu_frame = Frame(self.root, bg="#A29D9D", width=200)
        menu_frame.pack(side="left", fill="y")

        self.desenhar_eixos()

        # --- Criar objeto ---
        Label(menu_frame, text="Criar Objeto:", width=20, bg="#808080", fg="white",
              font=("Arial", 10, "bold")).pack(pady=(20, 5))

        criar_frame = Frame(menu_frame, bg="#808080")
        criar_frame.pack(pady=5)

        Button(criar_frame, text="Ponto", width=10, command=lambda: self.executar_objeto("Ponto")).grid(row=0, column=0, padx=2, pady=2)
        Button(criar_frame, text="Reta", width=10, command=lambda: self.executar_objeto("Reta")).grid(row=0, column=1, padx=2, pady=2)
        Button(criar_frame, text="Wireframe", width=10, command=lambda: self.executar_objeto("Wireframe")).grid(row=0, column=2, padx=2, pady=2)

        # --- Lista de objetos criados ---
        Label(menu_frame, text="Objetos criados:", width=20, bg="#808080", fg="white",
              font=("Arial", 10, "bold")).pack(pady=(20, 5))

        self.lista_objetos = Listbox(menu_frame, height=8, width=40, exportselection=False)
        self.lista_objetos.pack(padx=5)
        self.lista_objetos.bind("<<ListboxSelect>>", self.selecao_objeto)

        # --- Botão limpar tela ---
        Button(menu_frame, text="Limpar Tela", width=20, height=2, command=self.limpar_tela).pack(pady=10)

        # --- frame botões de movimento ---
        movimento_frame = Frame(menu_frame, bg="#808080")
        movimento_frame.pack(pady=5)

        btn_cima = Button(movimento_frame, text="CIMA", width=10, height=2,
                          command=lambda: self.mover_window(0, self.window.get_tam() / 8))
        btn_cima.grid(row=0, column=1, padx=5, pady=5)

        btn_esquerda = Button(movimento_frame, text="ESQUERDA", width=10, height=2,
                              command=lambda: self.mover_window(-self.window.get_tam() / 8, 0))
        btn_esquerda.grid(row=1, column=0, padx=(1), pady=5)

        btn_centralizar = Button(movimento_frame, text="CENTRALIZAR", width=10, height=2,
                                 command=lambda: self.centralizar_window())
        btn_centralizar.grid(row=1, column=1, padx=(1), pady=5)

        btn_direita = Button(movimento_frame, text="DIREITA", width=10, height=2,
                             command=lambda: self.mover_window(self.window.get_tam() / 8, 0))
        btn_direita.grid(row=1, column=2, padx=(1), pady=5)

        btn_baixo = Button(movimento_frame, text="BAIXO", width=10, height=2,
                           command=lambda: self.mover_window(0, -self.window.get_tam() / 8))
        btn_baixo.grid(row=2, column=1, padx=5, pady=5)

        # --- frame zoom ---
        zoom_frame = Frame(menu_frame, bg="#808080", pady=5)
        zoom_frame.pack(pady=5, padx=15)

        Label(zoom_frame, text="Zoom(%): ", bg="#808080", fg="white",
              font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        self.zoom_entry = Entry(zoom_frame, width=5)
        self.zoom_entry.insert(0, "0")
        self.zoom_entry.grid(row=0, column=1, padx=0)
        btn_zoom = Button(zoom_frame, text="Aplicar Zoom", command=self.aplicar_zoom)
        btn_zoom.grid(row=0, column=2, padx=50)

    def limpar_tela(self):
        self.canvas.delete("all")
        self.display_file.clear()
        self.redesenhar()

    def mover_window(self, dx, dy):
        self.window.mover(dx, dy)
        self.redesenhar()

    def centralizar_window(self):
        self.window.centralizar()
        self.redesenhar()

    def aplicar_zoom(self):
        try:
            fator = float(self.zoom_entry.get())
            self.window.zoom(fator)
            self.redesenhar()
        except ValueError:
            print("Digite um número válido para o zoom")

    def executar_objeto(self, tipo):
        if tipo == "Ponto":            
            nome_obj = simpledialog.askstring("Nome do objeto", "Digite um nome para o ponto:")
            entrada = simpledialog.askstring("Ponto", "Digite o ponto no formato: (x,y)")
            if entrada:
                try:
                    x, y = eval(entrada)
                    ponto = Ponto([(x, y)])
                    nome_final = nome_obj or f"Ponto{len(self.display_file) + 1}"
                    self.lista_obj.append((nome_final, ponto))
                    self.display_file.append((nome_final, ponto))
                    self.lista_objetos.insert(END, nome_final)
                except Exception:
                    print("Entrada inválida!")

        elif tipo == "Reta":            
            nome_obj = simpledialog.askstring("Nome do objeto", "Digite um nome para a reta:")
            entrada = simpledialog.askstring("Reta", "Digite os pontos no formato: (x1,y1),(x2,y2)")
            if entrada:
                try:
                    pontos = list(eval(f"[{entrada}]"))
                    if len(pontos) == 2:
                        reta = Reta(pontos)
                        nome_final = nome_obj or f"Reta{len(self.display_file) + 1}"
                        self.lista_obj.append((nome_final, reta))                        
                        self.display_file.append((nome_final, reta))
                        self.lista_objetos.insert(END, nome_final)
                except Exception:
                    print("Entrada inválida!")

        elif tipo == "Wireframe":            
            nome_obj = simpledialog.askstring("Nome do objeto", "Digite um nome para o wireframe:")
            entrada = simpledialog.askstring("Wireframe", "Digite os pontos no formato: (x1,y1),(x2,y2),...")
            if entrada:
                try:
                    pontos = list(eval(f"[{entrada}]"))
                    wire = Wireframe(pontos)
                    nome_final = nome_obj or f"Wire{len(self.display_file) + 1}"
                    self.lista_obj.append((nome_final, wire))
                    self.display_file.append((nome_final, wire))
                    self.lista_objetos.insert(END, nome_final)
                except Exception:
                    print("Entrada inválida!")

        self.redesenhar()
    
    def selecao_objeto(self, event):
        """Desenha apenas o objeto selecionado na tela"""
        idx = self.lista_objetos.curselection()
        if not idx:
            return
        nome = self.lista_objetos.get(idx)
        for nome_obj, obj in self.lista_obj:
            if nome_obj == nome:
                if (nome_obj, obj) not in self.display_file:
                    self.display_file.append((nome_obj, obj))
                self.redesenhar()
                break

    def redesenhar(self):
        self.canvas.delete("all")
        self.desenhar_eixos()
        for nome, obj in self.display_file:
            obj.desenhar(self.canvas, self.window, self.viewport)

    def desenhar_eixos(self):
        xv1, yv1 = self.viewport.world_to_viewport(0, -350, self.window)
        xv2, yv2 = self.viewport.world_to_viewport(0, 350, self.window)
        self.canvas.create_line(xv1, yv1, xv2, yv2, fill="gray", width=2, arrow='last')

        xv1, yv1 = self.viewport.world_to_viewport(-350, 0, self.window)
        xv2, yv2 = self.viewport.world_to_viewport(350, 0, self.window)
        self.canvas.create_line(xv1, yv1, xv2, yv2, fill="gray", width=2, arrow='last')

    def run(self):
        self.root.mainloop()

