from tkinter import *
from window import Window
from viewport import Viewport
from scn import SCN
from ponto import Ponto
from reta import Reta
from wireframe import Wireframe
from tkinter import simpledialog, messagebox
from tkinter.colorchooser import askcolor
import math

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
        self.scn = SCN()
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
         # Bind: clique direito
        self.lista_objetos.bind("<Button-3>", self.selecao_menu_objeto)

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

        # --- window rotation ---

        rotation_frame = Frame(menu_frame, bg="#808080", pady=5)
        rotation_frame.pack(pady=5, padx=15)
        Label(rotation_frame, text="Rodar Window: ", bg="#808080", fg="white",
              font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        btn_seta_esq = Button(rotation_frame, text="↶",font=("Segoe UI Symbol", 12, "bold"), width=4, height=2,
                           command=lambda: self.rotacionar_window("botao_esquerda"))
        btn_seta_esq.grid(row=0, column=1, padx=2, pady=2)

        btn_seta_dir = Button(rotation_frame, text="↷",font=("Segoe UI Symbol", 12, "bold"), width=4, height=2,
                           command=lambda: self.rotacionar_window("botao_direita"))
        btn_seta_dir.grid(row=0, column=2, padx=2, pady=2)
        Label(rotation_frame, text="Ângulo atual: ", bg="#808080", fg="white",
              font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5)
                # StringVar para mostrar o ângulo da window
        self.angulo_var = StringVar()
        self.angulo_var.set(f"{self.window.angulo:.1f}°")  # inicializa com valor atual

        # Label que mostra o valor do ângulo
        Label(rotation_frame, textvariable=self.angulo_var, bg="#808080", fg="white",
            font=("Arial", 10, "bold")).grid(row=1, column=1, columnspan=2, padx=5)



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
            valor = self.zoom_entry.get().strip()
            # Verifica se é número inteiro
            fator = int(valor)
            # Verifica se está no intervalo permitido
            if 0 <= fator <= 100:
                self.window.zoom(fator)
                self.redesenhar()
            else:
                messagebox.showerror(
                    "Erro", "Digite um número inteiro entre 0 e 100.",
                    parent=self.root)

        except ValueError:
            messagebox.showerror( "Erro", "Digite um número inteiro válido, entre 0 e 100.",
                parent=self.root)
            
    def rotacionar_window(self, direcao_botao):

        # Deve rotacionar para direita
        if direcao_botao == "botao_esquerda":
            self.window.angulo += 30
            
            
        # Deve rotacionar para esquerda
        else:
            self.window.angulo -= 30
            
        # atualiza label
        self.angulo_var.set(f"{self.window.angulo:.1f}°")

        self.redesenhar()
            

    def executar_objeto(self, tipo):
        if tipo == "Ponto":            
            nome_obj = simpledialog.askstring("Nome do objeto", "Digite um nome para o ponto:", parent=self.root)
            if nome_obj is None:  
                return 

            while True:
                entrada = simpledialog.askstring("Ponto", "Digite local do ponto no formato: (x,y)", parent=self.root)
                if entrada is None:  # usuário cancelou na segunda caixa
                    return
                
                if entrada.strip():
                    try:
                        x, y = eval(entrada)

                        # Abre seletor de cor
                        cor_escolhida = askcolor(title="Escolha a cor do ponto", parent=self.root)[1]
                        if cor_escolhida is None:  # se o usuário cancelar
                            cor_escolhida = "#E11919"
                        ponto = Ponto([(x, y)], cor_escolhida, self.window)
                        nome_final = nome_obj or f"Ponto{len(self.display_file) + 1}"
                        self.lista_obj.append((nome_final, ponto))
                        self.display_file.append((nome_final, ponto))
                        self.lista_objetos.insert(END, nome_final)
                        break

                    except Exception:
                        
                        messagebox.showerror("Erro", "Entrada inválida!\nDigite no formato (x,y).")
                else:
                        # Se o usuário só apertar Enter sem digitar nada
                    messagebox.showerror( "Erro", "Você precisa digitar no formato (x,y).",parent=self.root )

        elif tipo == "Reta":            
            nome_obj = simpledialog.askstring("Nome do objeto", "Digite um nome para a reta:", parent=self.root)
            if nome_obj is None:  
                return 
            while True:
                entrada = simpledialog.askstring("Reta", "Digite os pontos no formato: (x1,y1),(x2,y2)" , parent=self.root)
                if entrada is None:  # usuário cancelou na segunda caixa
                    return
                if entrada.strip():
                    try:
                        pontos = list(eval(f"[{entrada}]"))

                         # Abre seletor de cor
                        cor_escolhida = askcolor(title="Escolha a cor do ponto", parent=self.root)[1]
                        if cor_escolhida is None:  # se o usuário cancelar
                            cor_escolhida = "#E11919"

                        if len(pontos) == 2:
                            reta = Reta(pontos, cor_escolhida, self.window)
                            nome_final = nome_obj or f"Reta{len(self.display_file) + 1}"
                            self.lista_obj.append((nome_final, reta))                        
                            self.display_file.append((nome_final, reta))
                            self.lista_objetos.insert(END, nome_final)
                            break
                    except Exception:
                        #print("Entrada inválida!")
                        messagebox.showerror("Erro", "Entrada inválida!\nDigite os pontos no formato: (x1,y1),(x2,y2)")
                else:
                        # Se o usuário só apertar Enter sem digitar nada
                    messagebox.showerror( "Erro", "Você precisa digitar no formato (x1,y1),(x2,y2).",parent=self.root )
        elif tipo == "Wireframe":            
            nome_obj = simpledialog.askstring("Nome do objeto", "Digite um nome para o wireframe:", parent=self.root)
            if nome_obj is None:  
                return  
            while True:
                entrada = simpledialog.askstring("Wireframe", "Digite os pontos no formato: (x1,y1),(x2,y2),...", parent=self.root)
                if entrada is None:  # usuário cancelou na segunda caixa
                    return
                if entrada:
                    try:
                        pontos = list(eval(f"[{entrada}]"))

                         # Abre seletor de cor
                        cor_escolhida = askcolor(title="Escolha a cor do ponto", parent=self.root)[1]
                        if cor_escolhida is None:  # se o usuário cancelar
                            cor_escolhida = "#E11919"


                        wire = Wireframe(pontos, cor_escolhida, self.window)
                        nome_final = nome_obj or f"Wire{len(self.display_file) + 1}"
                        self.lista_obj.append((nome_final, wire))
                        self.display_file.append((nome_final, wire))
                        self.lista_objetos.insert(END, nome_final)
                        break
                    except Exception:
                        #print("Entrada inválida!")
                        messagebox.showerror("Erro", "Entrada inválida!\nDigite os pontos no formato: (x1,y1),(x2,y2),...")
                else:
                        # Se o usuário só apertar Enter sem digitar nada
                    messagebox.showerror( "Erro", "Você precisa digitar no formato (x1,y1),(x2,y2),...",parent=self.root )

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

    def selecao_menu_objeto(self, event):
        """Abre menu do objeto ao clicar nele com botão direito"""

        idx = self.lista_objetos.nearest(event.y)  # descobre em qual item foi clicado
        if idx >= 0:
            self.lista_objetos.selection_clear(0, END)
            self.lista_objetos.selection_set(idx)
            self.lista_objetos.activate(idx)

            nome = self.lista_objetos.get(idx)

                    # Recupera o objeto associado a esse nome
            objeto = None
            for nome_obj, obj in self.lista_obj:
                if nome_obj == nome:
                    objeto = obj
                    break

            if objeto is None:
                return  # não achou objeto correspondente
            
            # Adiciona menu para clique no objeto com botao direito
            menu = Menu(self.root, tearoff=0)
            menu.add_command(label="Transladar", command=lambda: self.modificar_objeto("Transladar", objeto,nome))
            menu.add_command(label="Escalonar", command=lambda: self.modificar_objeto("Escalonar", objeto,nome))
            menu.add_command(label="Rotacionar", command=lambda: self.modificar_objeto("Rotacionar", objeto,nome))

        # Abre o menu na posição do clique
            menu.tk_popup(event.x_root, event.y_root)

    def modificar_objeto(self, acao_escolhida, objeto,nome):
        
        if acao_escolhida == "Transladar":

            while True:
                entrada = simpledialog.askstring(nome, "Digite UM NOVO ponto no formato: (x1,y1)" , parent=self.root)
                if entrada is None:  # usuário cancelou a caixa
                    return
                if entrada.strip():
                    try:
                        dx, dy = map(int, entrada.strip("()").split(","))
                        objeto.transladar(dx/100, dy/100)

                        self.redesenhar()
                        break
                    except Exception:
                        messagebox.showerror("Erro", "Entrada inválida!\nDigite o ponto no formato: (x1,y1)")
                else:
                        # Se o usuário só apertar Enter sem digitar nada
                    messagebox.showerror( "Erro", "Você precisa digitar no formato (x1,y1)",parent=self.root )
            
        elif acao_escolhida == "Escalonar":
            while True:
                        entrada = simpledialog.askstring(
                            nome, 
                            "Digite os fatores de escala no formato: (sx,sy)", 
                            parent=self.root
                        )
                        if entrada is None:  # usuário cancelou
                            return
                        if entrada.strip():
                            try:
                                sx, sy = map(float, entrada.strip("()").split(","))
                                objeto.escalonar(sx, sy)
                                self.redesenhar()
                                break
                            except Exception:
                                messagebox.showerror(
                                    "Erro", 
                                    "Entrada inválida!\nDigite no formato: (sx,sy)"
                                )
                        else:
                            messagebox.showerror(
                                "Erro", 
                                "Você precisa digitar no formato (sx,sy)", 
                                parent=self.root
                            )
        elif acao_escolhida == "Rotacionar":

            popup = Toplevel(self.root)
            popup.title("Escolha uma opção de rotação")
            popup.geometry("300x250")

            escolha_var = StringVar(value="op1")

            # Radiobuttons
            Label(popup, text="Escolha uma opção:").pack(pady=5)
            Radiobutton(popup, text="Em torno do centro do mundo", variable=escolha_var, value="op1").pack(anchor="w")
            Radiobutton(popup, text="Em torno do centro do objeto", variable=escolha_var, value="op2").pack(anchor="w")
            Radiobutton(popup, text="Em torno de um ponto qualquer", variable=escolha_var, value="op3").pack(anchor="w")

            # Caixas de texto
            Label(popup, text="Digite o ângulo:").pack(pady=5)
            angulo_rotacao = Entry(popup, width=25)
            angulo_rotacao.pack()

            Label(popup, text="Digite o ponto, se necesário:").pack(pady=5)
            ponto_rotacao = Entry(popup,width = 25)
            ponto_rotacao.pack()

            def confirmar():
                angulo = angulo_rotacao.get().strip()
                ponto = ponto_rotacao.get().strip()
                acao = escolha_var.get()

                # valida angulo
                try:
                    ang = int(angulo)
                    if not (0 <= ang <= 360):
                        messagebox.showerror("Erro", "O ângulo deve ser um número inteiro entre 0 e 360.")
                        popup.lift()
                        popup.focus_force()
                        return
                except ValueError:
                    messagebox.showerror("Erro", "O ângulo deve ser um número inteiro entre 0 e 360.")
                    popup.lift()
                    popup.focus_force()
                    return

                cx, cy = 0, 0  # padrão: origem

                if acao == "op2":
                    # Rotação em torno do centro do objeto
                    cx, cy = objeto.centro()

                elif acao == "op3":
                    # Rotação em torno de ponto qualquer
                    try:
                        cx, cy = map(int, ponto.strip("() ").split(","))
                        cx /= 100
                        cy /= 100
                    except Exception:
                        messagebox.showerror("Erro", "Entrada inválida!\nDigite o ponto no formato: (x,y)")
                        popup.lift()
                        popup.focus_force()
                        return

                # chama a rotação correta
                objeto.rotacionar(ang, cx, cy)
                self.redesenhar()
                popup.destroy()

            Button(popup, text="Confirmar", command=confirmar).pack(pady=15)

    def redesenhar(self):
        self.canvas.delete("all")
        self.desenhar_eixos()
        for nome, obj in self.display_file:
            obj.desenhar(self.canvas, self.window, self.scn, self.viewport)

    def desenhar_eixos(self):
        ang = math.radians(self.window.angulo)

        # matriz de rotação
        cos_a = math.cos(ang)
        sin_a = math.sin(ang)

        def rot(x, y):
            xr = x * cos_a - y * sin_a
            yr = x * sin_a + y * cos_a
            return xr, yr

        # eixo Y (vertical no mundo, mas rotacionado pela window)
        x1, y1 = rot(0, -1)
        x2, y2 = rot(0,  1)
        xv1, yv1 = self.scn.world_to_scn_to_viewport(x1, y1, self.window, self.viewport)
        xv2, yv2 = self.scn.world_to_scn_to_viewport(x2, y2, self.window, self.viewport)
        self.canvas.create_line(xv1, yv1, xv2, yv2, fill="gray", width=2, arrow='last')

        # eixo X (horizontal no mundo, mas rotacionado pela window)
        x1, y1 = rot(-1, 0)
        x2, y2 = rot( 1, 0)
        xv1, yv1 = self.scn.world_to_scn_to_viewport(x1, y1, self.window, self.viewport)
        xv2, yv2 = self.scn.world_to_scn_to_viewport(x2, y2, self.window, self.viewport)
        self.canvas.create_line(xv1, yv1, xv2, yv2, fill="gray", width=2, arrow='last')



    def run(self):
        self.root.mainloop()

