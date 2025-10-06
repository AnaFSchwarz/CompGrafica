from tkinter import *
from window import Window
from viewport import Viewport
from scn import SCN
from ponto import Ponto
from reta import Reta
from wireframe import Wireframe
from curva import Curva
from ponto3D import Ponto3D
from tkinter import simpledialog, messagebox,filedialog
from tkinter.colorchooser import askcolor
import math
from descritor_obj import DescritorOBJ
from tkinter.filedialog import asksaveasfilename, askopenfilename

from objeto3D import ObjetoGrafico3D


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Sistema Gráfico Interativo 2D")
        self.root.geometry("1050x750")

        # Canvas
        self.canvas_width = 750
        self.canvas_height = 700
        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side="right", fill="both", expand=False)
        self.descritor = DescritorOBJ()

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
        menu_frame = Frame(self.root, bg="#F0F4F8", width=250)
        menu_frame.pack(side="left", fill="y")

        self.desenhar_eixos()

        # --- Criar objeto ---
        Label(menu_frame, text="Criar Objeto:", width=25, bg="#255A75", fg="white",
            font=("Arial", 10, "bold")).pack(pady=(10,2))
        
        criar_frame = Frame(menu_frame, bg="#F0F4F8")
        criar_frame.pack(pady=2, padx=20, fill='x')

        Button(criar_frame, text="Ponto", width=6, command=lambda: self.executar_objeto("Ponto")).grid(row=0, column=0, padx=2, pady=2)
        Button(criar_frame, text="Reta", width=6, command=lambda: self.executar_objeto("Reta")).grid(row=0, column=1, padx=2, pady=2)
        Button(criar_frame, text="Wireframe", width=9, command=lambda: self.executar_objeto("Wireframe")).grid(row=0, column=2, padx=2, pady=2)
        Button(criar_frame, text="Curva", width=6, command=lambda: self.executar_objeto("Curva")).grid(row=1, column=0, padx=2, pady=2)
        Button(criar_frame, text="Cubo padrão", width=6, command=lambda: self.executar_objeto("Cubo_padrao")).grid(row=1, column=1, padx=2, pady=2)

        # --- Lista de objetos com Scrollbar ---
        Label(menu_frame, text="Objetos criados:", width=25, bg="#255A75", fg="white",
            font=("Arial", 10, "bold")).pack(pady=(10,2))

        list_frame = Frame(menu_frame)
        list_frame.pack(pady=2, padx=5, fill='x')

        self.lista_objetos = Listbox(list_frame, height=8, width=30, exportselection=False)
        self.lista_objetos.pack(side='left', fill='both', expand=True)
        self.lista_objetos.bind("<<ListboxSelect>>", self.selecao_objeto)
        self.lista_objetos.bind("<Button-3>", self.selecao_menu_objeto)

        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        self.lista_objetos.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.lista_objetos.yview)

        # --- Limpar Tela (perto da lista) ---
        Button(menu_frame, text="Limpar Tela", width=20, command=self.limpar_tela).pack(pady=5)

        # --- Movimento (maior e centralizado) ---
        Label(menu_frame, text="Movimento:", width=25, bg="#255A75", fg="white",
            font=("Arial", 10, "bold")).pack(pady=(10,2))

        movimento_frame = Frame(menu_frame, bg="#F0F4F8")
        movimento_frame.pack(pady=2, padx=5)

        # Mantendo padrão maior e centralizado
        Button(movimento_frame, text="CIMA", width=12, height=2,
            command=lambda: self.mover_window(0, self.window.get_tam()/8)).grid(row=0, column=1, padx=2, pady=2)
        Button(movimento_frame, text="ESQUERDA", width=12, height=2,
            command=lambda: self.mover_window(-self.window.get_tam()/8,0)).grid(row=1, column=0, padx=2, pady=2)
        Button(movimento_frame, text="CENTRALIZAR", width=12, height=2,
            command=self.centralizar_window).grid(row=1, column=1, padx=2, pady=2)
        Button(movimento_frame, text="DIREITA", width=12, height=2,
            command=lambda: self.mover_window(self.window.get_tam()/8,0)).grid(row=1, column=2, padx=2, pady=2)
        Button(movimento_frame, text="BAIXO", width=12, height=2,
            command=lambda: self.mover_window(0,-self.window.get_tam()/8)).grid(row=2, column=1, padx=2, pady=2)

        # --- Zoom ---
        Label(menu_frame, text="Zoom (%):", width=25, bg="#255A75", fg="white",
            font=("Arial", 10, "bold")).pack(pady=(10,2))

        zoom_frame = Frame(menu_frame, bg="#F0F4F8")
        zoom_frame.pack(pady=2, padx=5, fill='x')

        self.zoom_entry = Entry(zoom_frame, width=15)
        self.zoom_entry.insert(0,"0")
        self.zoom_entry.pack(side='left', padx=5)
        Button(zoom_frame, text="Aplicar Zoom", width=15, command=self.aplicar_zoom).pack(side='left', padx=2)

        # --- Rotação Window ---
        Label(menu_frame, text="Rotação Window:", width=25, bg="#255A75", fg="white",
            font=("Arial", 10, "bold")).pack(pady=(10,2))

        rotation_frame = Frame(menu_frame, bg="#F0F4F8")
        rotation_frame.pack(pady=2, padx=5)

        Button(rotation_frame, text="↶", width=6, height=2,
            command=lambda: self.rotacionar_window("botao_esquerda")).grid(row=0, column=0, padx=2, pady=2)
        Button(rotation_frame, text="↷", width=6, height=2,
            command=lambda: self.rotacionar_window("botao_direita")).grid(row=0, column=1, padx=2, pady=2)
        self.angulo_var = StringVar(value=f"{self.window.angulo:.1f}°")
        Label(rotation_frame, textvariable=self.angulo_var, bg="#F0F4F8").grid(row=1, column=0, columnspan=2, pady=2)

        # --- Escolha do algoritmo de clipping --- 
        Label(menu_frame, text="Algoritmo de clipping retas", width=25, bg="#255A75", fg="white",
            font=("Arial", 10, "bold")).pack(pady=(10,2))
        self.tipo_clipping = IntVar(value=1)
        clipping_frame = Frame(menu_frame, bg="white")
        clipping_frame.pack(pady=(2,10), anchor="w")  # fica colado ao título e alinhado à esquerda

        Radiobutton(clipping_frame, text="Cohen-Sutherland",
                    variable=self.tipo_clipping, value=1,
                    bg="white").pack(side="left", padx=5)

        Radiobutton(clipping_frame, text="Liang–Barsky",
                    variable=self.tipo_clipping, value=2,
                    bg="white").pack(side="left", padx=5)
    

        # --- Exportar e Importar (mesma linha) ---
        final_frame = Frame(menu_frame, bg="#F0F4F8")
        final_frame.pack(side='bottom', pady=10, padx=5, fill='x')

        Button(final_frame, text="Exportar", width=12, command=self.exportar_obj).pack(side='left', padx=2)
        Button(final_frame, text="Importar", width=12, command=self.importar_obj).pack(side='left', padx=2)



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
                            cor_escolhida = "#1C19E1"
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
                            reta = Reta(pontos, cor_escolhida, self.window, self.tipo_clipping)
                            nome_final = nome_obj or f"Reta{len(self.display_file) + 1}"
                            self.lista_obj.append((nome_final, reta))                        
                            self.display_file.append((nome_final, reta))
                            self.lista_objetos.insert(END, nome_final)
                            break
                    except Exception:
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
                            cor_escolhida = "#19E15C"
                        wire = Wireframe(pontos, cor_escolhida, self.window)
                        nome_final = nome_obj or f"Wire{len(self.display_file) + 1}"
                        self.lista_obj.append((nome_final, wire))
                        self.display_file.append((nome_final, wire))
                        self.lista_objetos.insert(END, nome_final)
                        break

                    except Exception:
                        messagebox.showerror("Erro", "Entrada inválida!\nDigite os pontos no formato: (x1,y1),(x2,y2),...")
                else:
                        # Se o usuário só apertar Enter sem digitar nada
                    messagebox.showerror( "Erro", "Você precisa digitar no formato (x1,y1),(x2,y2),...",parent=self.root )

        elif tipo == "Curva":
            nome_obj = simpledialog.askstring("Nome do objeto", "Digite um nome para a curva:", parent=self.root)
            if nome_obj is None:  
                return  
            while True:
                entrada = simpledialog.askstring("Curva", "Digite 4 ou mais pontos no formato: (x1,y1),(x2,y2),(x3,y3)...", parent=self.root)
                if entrada is None:  # usuário cancelou na segunda caixa
                    return
                if entrada.strip():
                    try:
                        pontos = list(eval(f"[{entrada}]"))
                        # Abre seletor de cor
                        cor_escolhida = askcolor(title="Escolha a cor do ponto", parent=self.root)[1]
                        if cor_escolhida is None:  # se o usuário cancelar
                            cor_escolhida = "#C3E119"

                        if len(pontos) >= 4:
                            curva = Curva(pontos, cor_escolhida, self.window)
                            nome_final = nome_obj or f"Curva{len(self.display_file) + 1}"
                            self.lista_obj.append((nome_final, curva))
                            self.display_file.append((nome_final, curva))
                            self.lista_objetos.insert(END, nome_final)
                            break

                    except Exception:
                        messagebox.showerror("Erro", "Entrada inválida!\nDigite 4 pontos no formato: (x1,y1),(x2,y2),(x3,y3),(x4,y4)")
                else:
                        # Se o usuário só apertar Enter sem digitar nada
                    messagebox.showerror( "Erro", "Você precisa digitar no formato (x1,y1),(x2,y2),...",parent=self.root )
        elif tipo == "Cubo_padrao":
                # cria alguns pontos
                p1 = Ponto3D(1, 0, 0)
                p2 = Ponto3D(0, 1, 0)
                p3 = Ponto3D(0, 0, 1)

                # cria um objeto com esses pontos
                cubo = ObjetoGrafico3D([p1, p2, p3])

                print("Antes da rotação:")
                print(cubo)

                cubo.rotacionar_z(90)

                print("\nDepois da rotação em Z:")
                print(cubo)

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
            obj.tipo_clipping = self.tipo_clipping
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

        # caixa de window
        corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        pts = []
        for x, y in corners:
            xr, yr = rot(x, y)
            xv, yv = self.scn.world_to_scn_to_viewport(xr, yr, self.window, self.viewport)
            pts.extend([xv, yv])

        self.canvas.create_polygon(pts, outline="red", fill="", width=3)


    def exportar_obj(self):
        if not self.display_file:
            messagebox.showinfo("Info", "Não há objetos para exportar.")
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".obj", filetypes=[("Wavefront OBJ", "*.obj")])
        if not filename:
            return
        try:
            self.descritor.exportar(self.display_file, filename)
            messagebox.showinfo("Exportar", f"Arquivo exportado com sucesso:\n{filename}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar:\n{e}")

    def importar_obj(self):
        filename = filedialog.askopenfilename(filetypes=[("Wavefront OBJ", "*.obj")])
        if not filename:
            return
        try:
            objs_importados = self.descritor.importar(filename, self.window)
            for nome, obj in objs_importados:
                self.lista_obj.append((nome, obj))
                self.display_file.append((nome, obj))
                self.lista_objetos.insert(END, nome)
            self.redesenhar()
            messagebox.showinfo("Importar", f"{len(objs_importados)} objetos importados com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao importar:\n{e}")


    def run(self):
        self.root.mainloop()

