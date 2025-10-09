from typing import List, Tuple, Any
from ponto import Ponto
from reta import Reta
from wireframe import Wireframe

class DescritorOBJ:
    def __init__(self):
        pass

    # ---------- Escrita ----------
    def exportar(self, objeto_selecionado, nome, filename: str):
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

            object_blocks.append({
                'name': nome,
                'color': color,
                'indices': indices,
                'tipo': type(objeto_selecionado).__name__
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
                if blk['tipo'] == 'Ponto' or len(blk['indices']) == 1:
                    f.write(f"p {blk['indices'][0]}\n")
                else:
                    indices_str = " ".join(str(i) for i in blk['indices'])
                    f.write(f"l {indices_str}\n")
                f.write("\n")

    # ---------- Leitura ----------
    def importar(self, filename: str, window) -> List[Tuple[str, Any]]:
        """
        Lê um .obj e retorna lista de (nome, objeto) usando Ponto, Reta ou Wireframe.
        """
        verts: List[Tuple[float, float]] = []
        objs = []
        current_name = None
        current_color = None

        def flush_pending(indices):
            nonlocal objs, current_name, current_color
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
            objs.append((name, obj))
            # reset
            current_name = None
            current_color = None

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
