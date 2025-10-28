from tkinter import *
from window import Window
from viewport import Viewport
from scn import SCN
from objeto import ObjetoGrafico
from ponto import Ponto
from reta import Reta
from wireframe import Wireframe
from curva import Curva
from tkinter import simpledialog, messagebox,filedialog
from tkinter.colorchooser import askcolor
import math
from descritor_obj import DescritorOBJ
from objeto3D import ObjetoGrafico3D
from ponto3D import Ponto3D
from superficiebicubica import SuperficieBezier
from functools import partial


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Sistema Gráfico Interativo 2D - Grupo 2")
        try:
            self.root.state('zoomed')
        except:
            self.root.attributes('-zoomed', True)

        # Canvas
        self.canvas_width = 750
        self.canvas_height = 700
        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side="right", fill="both", expand=True)
        self.descritor = DescritorOBJ()

        # Window e Viewport
        self.window = Window()
        self.scn = SCN()
        self.viewport = Viewport(0, self.canvas_width, 0, self.canvas_height)

        # Display file
        self.display_file = []
        self.lista_obj = []

        self.lista_obj3D = []
        self.display_file3D = []
        
        # Menu lateral
        self._criar_menu()

        self.run()


    def _criar_menu(self):
        menu_frame = Frame(self.root, bg="#F0F4F8", width=250)
        menu_frame.pack(side="left", fill="y")

        # --- Criar objeto ---
        Label(menu_frame, text="Criar Objeto:", width=35, bg="#255A75", fg="white",
            font=("Arial", 10, "bold")).pack(pady=(10,2))
        
        criar_frame = Frame(menu_frame, bg="#F0F4F8")
        criar_frame.pack(pady=2, padx=20, fill='x')

        Button(criar_frame, text="Ponto", width=6, command=lambda: self.executar_objeto("Ponto")).grid(row=0, column=0, padx=2, pady=2)
        Button(criar_frame, text="Reta", width=6, command=lambda: self.executar_objeto("Reta")).grid(row=0, column=1, padx=2, pady=2)
        Button(criar_frame, text="Wireframe", width=9, command=lambda: self.executar_objeto("Wireframe")).grid(row=0, column=2, padx=2, pady=2)
        Button(criar_frame, text="Curva", width=6, command=lambda: self.executar_objeto("Curva")).grid(row=1, column=0, padx=2, pady=2)
        Button(criar_frame, text="Objeto3D", width=9, command=lambda: self.executar_objeto("Objeto3D")).grid(row=1, column=1, padx=2, pady=2)
        Button(criar_frame, text="SupBic", width=9, command=lambda: self.executar_objeto("SupBic")).grid(row=1, column=2, padx=2, pady=2)
        
        # --- Lista de objetos com Scrollbar ---
        Label(menu_frame, text="Objetos criados:", width=35, bg="#255A75", fg="white",
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

        Label(menu_frame, text="* Altere os objetos clicando com botão direito *", width=35, bg="#E5EAEC", fg="Black",
            font=("Arial", 10)).pack(pady=(20,2))

        # --- Limpar Tela (perto da lista) ---
        Button(menu_frame, text="Limpar Tela", width=20, command=self.limpar_tela).pack(pady=5)

        # --- Movimento (maior e centralizado) ---
        Label(menu_frame, text="Movimento:", width=35, bg="#255A75", fg="white",
            font=("Arial", 10, "bold")).pack(pady=(10,2))

        movimento_frame = Frame(menu_frame, bg="#F0F4F8")
        movimento_frame.pack(pady=2, padx=5)

        # Mantendo padrão maior e centralizado
        Button(movimento_frame, text="CIMA", width=12, height=1,
            command=lambda: self.mover_window(0, self.window.get_tam()/8)).grid(row=0, column=1, padx=2, pady=2)
        Button(movimento_frame, text="ESQUERDA", width=12, height=1,
            command=lambda: self.mover_window(-self.window.get_tam()/8,0)).grid(row=1, column=0, padx=2, pady=2)
        Button(movimento_frame, text="CENTRALIZAR", width=12, height=1,
            command=self.centralizar_window).grid(row=1, column=1, padx=2, pady=2)
        Button(movimento_frame, text="DIREITA", width=12, height=1,
            command=lambda: self.mover_window(self.window.get_tam()/8,0)).grid(row=1, column=2, padx=2, pady=2)
        Button(movimento_frame, text="BAIXO", width=12, height=1,
            command=lambda: self.mover_window(0,-self.window.get_tam()/8)).grid(row=2, column=1, padx=2, pady=2)

        # --- Zoom ---
        Label(menu_frame, text="Zoom (%):", width=35, bg="#255A75", fg="white",
            font=("Arial", 10, "bold")).pack(pady=(10,2))

        zoom_frame = Frame(menu_frame, bg="#F0F4F8")
        zoom_frame.pack(pady=2, padx=2, fill='x')

        # Barra deslizante de 0 a 100, valor inicial 15
        self.zoom_var = IntVar(value=15)
        self.zoom_scale = Scale(zoom_frame, from_=0, to=100, orient='horizontal', variable=self.zoom_var, bg="#F0F4F8", highlightthickness=0,troughcolor="#d0e0ea",           length=180,
            command=lambda val: self.redesenhar())
        self.zoom_scale.pack(side='left', padx=5, fill='x', expand=True)

        # --- Rotação Window ---
        Label(menu_frame, text="Rotação Window:", width=35, bg="#255A75", fg="white",
            font=("Arial", 10, "bold")).pack(pady=(10,2))

        rotation_frame = Frame(menu_frame, bg="#F0F4F8")
        rotation_frame.pack(pady=1, padx=5)

        Button(rotation_frame, text="↶", width=6, height=1,
            command=lambda: self.rotacionar_window("botao_esquerda")).grid(row=0, column=0, padx=2, pady=2)
        Button(rotation_frame, text="↷", width=6, height=1,
            command=lambda: self.rotacionar_window("botao_direita")).grid(row=0, column=1, padx=2, pady=2)
        self.angulo_var = StringVar(value=f"{self.window.angulo:.1f}°")
        Label(rotation_frame, textvariable=self.angulo_var, bg="#F0F4F8").grid(row=1, column=0, columnspan=2, pady=2)

        # --- Escolha do algoritmo de clipping --- 
        Label(menu_frame, text="Algoritmo de clipping retas", width=35, bg="#255A75", fg="white",
            font=("Arial", 10, "bold")).pack(pady=(10,2))
        self.tipo_clipping = IntVar(value=1)
        clipping_frame = Frame(menu_frame, bg="white")
        clipping_frame.pack(pady=(2,10), anchor="w")  

        Radiobutton(clipping_frame, text="Cohen-Sutherland",
                    variable=self.tipo_clipping, value=1,
                    bg="white").pack(side="left", padx=3)

        Radiobutton(clipping_frame, text="Liang–Barsky",
                    variable=self.tipo_clipping, value=2,
                    bg="white").pack(side="left", padx=3)
    

        # --- Importar 2D e 3D ---
        final_frame = Frame(menu_frame, bg="#F0F4F8")
        final_frame.pack(side='bottom', pady=10, padx=5, fill='x')
        Button(final_frame, text="Importar 2D", width=12, command=partial(self.importar_obj, "2D", acao="clique")).pack(side='left', padx=2)
        Button(final_frame, text="Importar 3D", width=12, command=partial(self.importar_obj, "3D",  acao="clique")).pack(side='left', padx=4)
        
        self.desenhar_eixos()

        self.criar_objetos_basicos()

    def criar_objetos_basicos(self):

        self.importar_obj("2D", filename="objetos_criados/Ponto2.obj")
        self.importar_obj("2D", filename="objetos_criados/Reta2.obj")
        self.importar_obj("2D", filename="objetos_criados/Casa2.obj")
        self.importar_obj("3D", filename="objetos_criados/CuboMagic1.obj")
        self.importar_obj("3D", filename="objetos_criados/Piramide3D6.obj")
        self.importar_obj("3D", filename="objetos_criados/Paralelepipedo2.obj")
        self.importar_obj("3D", filename="objetos_criados/SupBicubicaTeste.obj")
        self.importar_obj("3D", filename="objetos_criados/Xicara2.obj")
        self.importar_obj("3D", filename="objetos_criados/diamante2.obj")

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
        
        elif tipo == "Objeto3D":
            nome_obj = simpledialog.askstring("Nome do objeto", "Digite um nome para o Objeto3D:", parent=self.root)
            if nome_obj is None:
                return  

            while True:
                entrada = simpledialog.askstring(
                    "Objeto3D",
                    "Digite as arestas no formato: (x1,y1,z1),(x2,y2,z2); (x3,y3,z3),(x4,y4,z4)...",
                    parent=self.root
                )
                if entrada is None:
                    return
                if entrada.strip():
                    try:
                        # Quebra em pares de pontos
                        segmentos_raw = [s.strip() for s in entrada.split(";") if s.strip()]
                        pontos_dict = {}  # para evitar duplicatas
                        arestas = []
                        for seg in segmentos_raw:
                            # garante que contém dois pontos
                            if "),(" not in seg:
                                raise ValueError(f"Segmento mal formatado: {seg}")

                            p1_str, p2_str = seg.split("),(")
                            p1 = tuple(map(float, p1_str.strip(" ()").split(",")))
                            p2 = tuple(map(float, p2_str.strip(" ()").split(",")))

                            for p in [p1, p2]:
                                if p not in pontos_dict:
                                    pontos_dict[p] = len(pontos_dict)
                            
                            arestas.append((pontos_dict[p1], pontos_dict[p2]))
                        
                        pontos = list(pontos_dict.keys())

                        cor_escolhida = askcolor(title="Escolha a cor do objeto", parent=self.root)[1]
                        if cor_escolhida is None:
                            cor_escolhida = "#000000"

                        obj3d = ObjetoGrafico3D(pontos, cor_escolhida, arestas, self.window)
                        nome_final = nome_obj or f"Objeto3D{len(self.display_file) + 1}"
                        self.lista_obj.append((nome_final, obj3d))
                        self.display_file.append((nome_final, obj3d))
                        self.lista_objetos.insert(END, nome_final)
                        break

                    except Exception as e:
                        messagebox.showerror("Erro", f"Entrada inválida!\n{e}")
                else:
                    messagebox.showerror("Erro", "Você precisa digitar no formato (x1,y1,z1),(x2,y2,z2); ...", parent=self.root)
            
        elif tipo == "SupBic":

            #  ETAPA 1: Nome e tamanho 
            self.janela = Toplevel(self.root)
            self.janela.title("Superfície Bicúbica de Bézier - Etapa 1")

            largura, altura = 500, 300
            x = (self.janela.winfo_screenwidth() - largura) // 2
            y = (self.janela.winfo_screenheight() - altura) // 2
            self.janela.geometry(f"{largura}x{altura}+{x}+{y}")

            Label(
                self.janela,
                text="Configuração da Superfície Bicúbica de Bézier",
                font=("Arial", 14, "bold")
            ).pack(pady=15)

            frame_config = Frame(self.janela)
            frame_config.pack(pady=20)

            Label(frame_config, text="Nome do objeto (opcional):", font=("Arial", 11)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
            nome_entry = Entry(frame_config, width=25)
            nome_entry.grid(row=0, column=1)

            # Menu de opções fixas para tamanho
            Label(frame_config, text="Tamanho da matriz:", font=("Arial", 11)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
            tamanhos = [f"{i}x{i}" for i in range(4, 21)]
            tamanho_var = StringVar(value=tamanhos[0])
            OptionMenu(frame_config, tamanho_var, *tamanhos).grid(row=1, column=1, pady=5)

            def avancar_para_matriz():
                #Avança para a segunda etapa: preenchimento da matriz.
                nome_obj = nome_entry.get().strip()
                n = int(tamanho_var.get().split("x")[0])

                self.janela.destroy()

                #  ETAPA 2: Preenchimento da matriz
                janela2 = Toplevel(self.root)
                janela2.title(f"Superfície Bézier - Etapa 2 ({n}x{n})")

                largura2, altura2 = 900, 700
                x2 = (janela2.winfo_screenwidth() - largura2) // 2
                y2 = (janela2.winfo_screenheight() - altura2) // 2
                janela2.geometry(f"{largura2}x{altura2}+{x2}+{y2}")

                Label(
                    janela2,
                    text=f"Preencha os pontos de controle ({n}x{n}):",
                    font=("Arial", 13, "bold")
                ).pack(pady=10)

                frame_matriz = Frame(janela2)
                frame_matriz.pack(pady=10)

                entradas = []
                for i in range(n):
                    linha = []
                    for j in range(n):
                        campo = Entry(frame_matriz, width=18, font=("Consolas", 10))
                        campo.insert(0, "0.0, 0.0, 0.0")
                        campo.grid(row=i, column=j, padx=3, pady=3)
                        linha.append(campo)
                    entradas.append(linha)

                def confirmar():
                    #Lê os pontos e cria a superfície
                    matriz = []
                    for linha_entries in entradas:
                        linha = []
                        for campo in linha_entries:
                            texto = campo.get()
                            try:
                                x, y, z = map(float, texto.replace(" ", "").split(","))
                                linha.append([x, y, z])
                            except Exception:
                                linha.append([0.0, 0.0, 0.0])
                        matriz.append(linha)

                    try:
                        sup = SuperficieBezier(matrizes_controle=[matriz], cor="blue", window=self.root)
                        nome_final = nome_obj or f"SuperficieBezier{len(self.display_file) + 1}"
                        self.lista_obj.append((nome_final, sup))
                        self.display_file.append((nome_final, sup))
                        self.lista_objetos.insert(END, nome_final)
                        
                    except Exception as e:
                        print("Erro ao criar superfície:", e)

                    janela2.destroy()

                Button(janela2,text="Confirmar Superfície",command=confirmar,width=20,bg="#d0f0d0",font=("Arial", 10, "bold")).pack(pady=15)

            Button(self.janela,text="Avançar para Preenchimento",command=avancar_para_matriz,width=25,bg="#e0f0ff",font=("Arial", 10, "bold")).pack(pady=25)

        self.redesenhar()

    # Para Superficie Bicubica 3D
    def adicionar_retalho(self):
        #Adiciona uma nova matriz 4x4 de entradas
        idx = len(self.matrizes_frames) + 1
        frame = LabelFrame(self.frame_scroll, text=f"Retalho {idx}", padx=6, pady=6)
        frame.pack(padx=10, pady=8, fill="x")

        entradas = []
        for i in range(4):
            linha = []
            for j in range(4):
                e = Entry(frame, width=18, justify="center")
                e.insert(0, f"{i},{j},0")  # valor inicial padrão
                e.grid(row=i, column=j, padx=3, pady=3)
                linha.append(e)
            entradas.append(linha)
        self.matrizes_frames.append(entradas)

    #Para superficie bicubica 3D
    def confirmar(self):
        #Lê todos os retalhos e envia como lista de matrizes
        todas_matrizes = []
        try:
            for entradas in self.matrizes_frames:
                matriz = []
                for i in range(4):
                    linha = []
                    for j in range(4):
                        txt = entradas[i][j].get().strip()
                        x, y, z = map(float, txt.replace("(", "").replace(")", "").split(","))
                        linha.append((x, y, z))
                    matriz.append(linha)
                todas_matrizes.append(matriz)

            self.self.janela.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Entrada inválida!\nUse o formato: x,y,z\n\nDetalhe: {e}")

    
    def selecao_objeto(self, event):
        #Desenha apenas o objeto selecionado na tela
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
        #Abre menu do objeto ao clicar nele com botão direito

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
            menu.add_command(label="Exportar", command=lambda: self.exportar_obj(objeto, nome))

        # Abre o menu na posição do clique
            menu.tk_popup(event.x_root, event.y_root)

    def modificar_objeto(self, acao_escolhida, objeto, nome):
        
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
                    except Exception as e:
                        messagebox.showerror("Erro", f"Entrada inválida!\nDigite o ponto no formato: (x1,y1)\n{e}")
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
                            except Exception as e:
                                messagebox.showerror(
                                    "Erro", 
                                    f"Entrada inválida!\nDigite no formato: (sx,sy)\n{e}"
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
            popup.geometry("300x400")

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

                cx, cy, cz = 0, 0, 0 # padrão: origem

                if acao == "op2" and isinstance(objeto, ObjetoGrafico):
                    # Rotação em torno do centro do objeto
                    cx, cy = objeto.centro()

                elif acao == "op2" and isinstance(objeto, ObjetoGrafico3D):
                    cx, cy, cz = objeto.centro()

                elif acao == "op3":
                    # Rotação em torno de ponto qualquer
                    try:
                        cx, cy = map(int, ponto.strip("() ").split(","))
                        cx /= 100
                        cy /= 100
                        #cz /= 100
                    except Exception:
                        messagebox.showerror("Erro", "Entrada inválida!\nDigite o ponto no formato: (x,y)")
                        popup.lift()
                        popup.focus_force()
                        return

                # chama a rotação correta
                if isinstance(objeto, ObjetoGrafico):
                    objeto.rotacionar(ang, cx, cy)
                #3D
                else:
                    objeto.rotacionar(ang, cx, cy, cz)
                self.redesenhar()
                popup.destroy()

            Button(popup, text="Confirmar", command=confirmar).pack(pady=15)

    def redesenhar(self):

        self.canvas.delete("all")
        self.desenhar_eixos()
        for nome, obj in self.display_file:
            if isinstance(obj, ObjetoGrafico3D):
                # projeção ortogonal do 3D para 2D
                obj.desenhar(self.canvas, self.window, self.scn, self.viewport)
            else:
                obj.tipo_clipping = self.tipo_clipping
                obj.desenhar(self.canvas, self.window, self.scn, self.viewport)

    def desenhar_eixos(self):

        #aplicar zoom
        fator = self.zoom_var.get()
        self.window.zoom(fator)

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


    def exportar_obj(self, objeto_selecionado, nome_objeto):

        if isinstance(objeto_selecionado, ObjetoGrafico) :
            filename = filedialog.asksaveasfilename(
                defaultextension=".obj", filetypes=[("Wavefront OBJ", "*.obj")])
            if not filename:
                return
            try:
                self.descritor.exportar_2D(objeto_selecionado, nome_objeto, filename)
                messagebox.showinfo("Exportar", f"Arquivo exportado com sucesso:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao exportar:\n{e}")

        elif isinstance(objeto_selecionado,ObjetoGrafico3D):
            filename = filedialog.asksaveasfilename(
                defaultextension=".obj", filetypes=[("Wavefront OBJ", "*.obj")])
            if not filename:
                return
            try:
                self.descritor.exportar_3D(objeto_selecionado, nome_objeto, filename)
                messagebox.showinfo("Exportar", f"Arquivo exportado com sucesso:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao exportar:\n{e}")
    

    def importar_obj(self, botao, filename=None, acao=None):

        if filename is None:
            filename = filedialog.askopenfilename(filetypes=[("Wavefront OBJ", "*.obj")])
        if not filename:
            return
        try:
            if botao == "2D":
                objs_importados = self.descritor.importar2D(filename, self.window)
            else:
                objs_importados = self.descritor.importar3D(filename, self.window)
            for nome, obj in objs_importados:
                self.lista_obj.append((nome, obj))
                self.display_file.append((nome, obj))
                self.lista_objetos.insert(END, nome)
            self.redesenhar()
            if (acao is not None):
                messagebox.showinfo("Importar", f"{len(objs_importados)} objeto importado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao importar 3D:\n{e}")


    def run(self):
        self.root.mainloop()

