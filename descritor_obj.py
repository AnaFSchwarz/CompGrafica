from typing import List, Tuple, Any
from ponto import Ponto
from reta import Reta
from wireframe import Wireframe
from objeto3D import ObjetoGrafico3D

class DescritorOBJ:
    def __init__(self):
        pass

    # ---------- Escrita ----------
    def exportar_2D(self, objeto_selecionado, nome, filename: str):
        """
        Gera um .obj com todos os vértices e linhas (l) por objeto.
        """
        vertices = []  # lista global de (x,y)
        object_blocks = []

        pts = [[coord * 100 for coord in ponto] for ponto in objeto_selecionado.pontos]

        if pts:  # só processa se houver pontos
            start_index = len(vertices) + 1
            indices = list(range(start_index, start_index + len(pts)))
            vertices.extend(pts)

            color = getattr(objeto_selecionado, 'cor', None)
            tipo_clipping = getattr(objeto_selecionado, 'tipo_clipping', None)

            object_blocks.append({
                'name': nome,
                'color': color,
                'indices': indices,
                'tipo': type(objeto_selecionado).__name__,
                'tipo_clipping': tipo_clipping
        })

        # escreve arquivo
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Exported by DescritorOBJ\n")
            for x, y in vertices:
                f.write(f"v {x:.6f} {y:.6f} 0.0\n")
            f.write("\n")

            for blk in object_blocks:
                f.write(f"# name: {blk['name']}\n")
                if blk['color']:
                    f.write(f"# color: {blk['color']}\n")
                if blk['tipo_clipping']:
                    f.write(f"# tipo_clipping: {blk['tipo_clipping']}\n")
                if blk['tipo'] == 'Ponto' or len(blk['indices']) == 1:
                    f.write(f"p {blk['indices'][0]}\n")
                else:
                    indices_str = " ".join(str(i) for i in blk['indices'])
                    f.write(f"l {indices_str}\n")
                f.write("\n")

    def exportar_3D(self, objeto_selecionado, nome, filename: str):
        """
        Exporta um único objeto 3D no formato .obj, incluindo vértices (v),
        arestas (l) e metadados (cor, tipo_clipping).
        """
        # Coleta vértices e arestas do objeto
        vertices = [tuple(map(lambda c: c * 100, p)) for p in objeto_selecionado.pontos]
        arestas = getattr(objeto_selecionado, "arestas", [])
        color = getattr(objeto_selecionado, "cor", None)
        tipo_clipping = getattr(objeto_selecionado, "tipo_clipping", None)

        with open(filename, "w", encoding="utf-8") as f:

            # Vértices
            for x, y, z in vertices:
                f.write(f"v {x:.6f} {y:.6f} {z:.6f}\n")
            f.write("\n")

            # Arestas (usando índice 1-based conforme padrão OBJ)
            for a, b in arestas:
                f.write(f"l {a+1} {b+1}\n")
            f.write("\n")

            f.write("# Exported by DescritorOBJ 3D\n")
            f.write(f"# name: {nome}\n")
            if color:
                f.write(f"# color: {color}\n")
            if tipo_clipping:
                f.write(f"# tipo_clipping: {tipo_clipping}\n")
            f.write("\n")

            # Cabeçalho do objeto
            f.write(f"o {nome}\n")

    # ---------- Leitura ----------
    def importar2D(self, filename: str, window) -> List[Tuple[str, Any]]:
        """
        Lê um .obj e retorna lista de (nome, objeto) usando Ponto, Reta ou Wireframe.
        """
        verts: List[Tuple[float, float]] = []
        objs = []
        current_name = None
        current_color = None
        current_tipo_clipping = None

        def flush_pending(indices):
            nonlocal objs, current_name, current_color, current_tipo_clipping
            pts = [verts[i - 1] for i in indices if 1 <= i <= len(verts)]
            if not pts:
                return
            name = current_name or f"Obj{len(objs)+1}"
            color = current_color or "#E11919"
            if len(pts) == 1:
                obj = Ponto([pts[0]], color, window)
            elif len(pts) == 2:
                obj = Reta(pts, color, window)
            else:
                obj = Wireframe(pts, color, window)

             # Adiciona metadado opcional (tipo_clipping)
            if current_tipo_clipping is not None:
                setattr(obj, "tipo_clipping", current_tipo_clipping)

            objs.append((name, obj))
            # reset
            current_name = None
            current_color = None
            current_tipo_clipping = None

        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    if ':' in line:
                        key, val = line[1:].split(':', 1)
                        key = key.strip().lower()
                        val = val.strip()
                        if key == 'name':
                            current_name = val
                        elif key == 'color':
                            current_color = val
                   
                    continue
                parts = line.split()
                if not parts:
                    continue
                if parts[0] == 'v' and len(parts) >= 3:
                    try:
                        x = float(parts[1])
                        y = float(parts[2])
                        verts.append((x, y))
                    except:
                        pass
                elif parts[0] in ('p', 'l', 'f'):
                    try:
                        indices = [int(x.split('/')[0]) for x in parts[1:]]
                        flush_pending(indices)
                    except:
                        pass
        return objs


    def importar3D(self, filename: str, window) -> List[Tuple[str, Any]]:
        """
        Lê um .obj e retorna lista de (nome, ObjetoGrafico3D) com pontos, arestas e metadados.
        """
        verts: List[Tuple[float, float, float]] = []
        arestas_correntes: List[Tuple[int, int]] = []
        objs = []
        current_name = None
        current_color = None
        current_tipo_clipping = None

        def flush_pending():
            """
            Cria um ObjetoGrafico3D com os vértices e arestas coletadas.
            """
            nonlocal verts, arestas_correntes, objs, current_name, current_color, current_tipo_clipping
            if not verts:
                return

            name = current_name or f"Objeto3D{len(objs)+1}"
            color = current_color or "#000000"

            obj = ObjetoGrafico3D(list(verts), color, list(arestas_correntes), window)

            if current_tipo_clipping is not None:
                setattr(obj, "tipo_clipping", current_tipo_clipping)

            objs.append((name, obj))

            # Reseta listas e contexto
            verts = []
            arestas_correntes = []
            current_name = None
            current_color = None
            current_tipo_clipping = None

        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Comentários com metadados
                if line.startswith('#'):
                    if ':' in line:
                        key, val = line[1:].split(':', 1)
                        key = key.strip().lower()
                        val = val.strip()
                        if key == 'name':
                            current_name = val
                        elif key == 'color':
                            current_color = val
                        elif key == 'tipo_clipping':
                            current_tipo_clipping = int(val)
                    continue

                parts = line.split()
                if not parts:
                    continue

                # Vértices
                if parts[0] == 'v' and len(parts) >= 4:
                    try:
                        x, y, z = map(float, parts[1:4])
                        verts.append((x, y, z))
                    except ValueError:
                        continue

                # Linhas (arestas)
                elif parts[0] == 'l':
                    try:
                        indices = [int(x) - 1 for x in parts[1:]]  # converte para 0-based
                        # Cria pares consecutivos como arestas
                        for i in range(len(indices) - 1):
                            arestas_correntes.append((indices[i], indices[i+1]))
                    except Exception:
                        continue

                # Quando encontrar novo objeto, finaliza o anterior
                elif parts[0] == 'o':
                    flush_pending()

            # Garante que o último objeto seja adicionado
            flush_pending()

        return objs

