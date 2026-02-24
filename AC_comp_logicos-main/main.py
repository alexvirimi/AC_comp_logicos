"""
Este módulo implementa una consola interactiva que permite construir y evaluar
un circuito lógico representado como un árbol binario perfecto. El usuario puede
definir la cantidad de niveles (hasta 6), seleccionar el tipo de compuerta por
nivel, asignar valores a las entradas (hojas), agregar opcionalmente un Flip-Flop
SR en cualquier nodo (ya sea en su entrada o salida), evaluar el circuito y
visualizar tanto su estructura como el resultado final. Para integrarlo en una
interfaz gráfica, bastaría con reemplazar las entradas por consola por elementos
visuales como formularios, listas desplegables y botones, reutilizando directamente
la lógica de construcción (TreeBuilder), evaluación (evaluate_with_flipflop) y
representación estructural del árbol.
"""

# Importa las compuertas disponibles y el FlipFlop desde el módulo de compuertas
from gates import AND, OR, NAND, NOR, XOR, FlipFlop

# Importa la clase Nodo que representa cada nodo del árbol lógico
from tree.node import Nodo

# Importa el constructor del árbol lógico
from tree.builder import TreeBuilder


# Diccionario que asocia el nombre textual de cada compuerta con su clase correspondiente
# Permite seleccionar dinámicamente el tipo de compuerta en cada nivel
GATE_MAP = {
    'AND': AND,
    'OR': OR,
    'NAND': NAND,
    'NOR': NOR,
    'XOR': XOR,
}


# Imprime una línea separadora en consola, opcionalmente con un título centrado
# Se utiliza para organizar visualmente las secciones del programa
def print_separator(title: str = ""):
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print("-" * 60)


# Devuelve un bit coloreado para visualización en consola
# 1 se muestra en verde y 0 en rojo usando códigos ANSI
def color_bit(b: int) -> str:
    if b == 1:
        return f"\x1b[32m1\x1b[0m"
    return f"\x1b[31m0\x1b[0m"


# Imprime recursivamente el árbol lógico mostrando cada nodo y su resultado
# Las hojas muestran su valor, y los nodos internos muestran la compuerta y su salida
def print_tree(node: Nodo, prefix: str = ""):
    if node is None:
        return

    if node.is_leaf():
        val = node.value if node.result is None else node.result
        print(f"{prefix} Hoja (val={color_bit(int(val))})")
    else:
        gate_name = node.gate.__class__.__name__
        res = node.result if node.result is not None else "?"
        res_str = color_bit(int(res)) if isinstance(res, int) else res
        print(f"{prefix} {gate_name} -> {res_str}")

    if node.left is not None:
        print_tree(node.left, prefix + "  ├─ ")
    if node.right is not None:
        print_tree(node.right, prefix + "  └─ ")


# Permite obtener un nodo específico del árbol usando una ruta basada en L (left) y R (right)
# Por ejemplo: "" es la raíz, "L" es el hijo izquierdo, "RL" es derecha-izquierda
def get_node_by_path(root: Nodo, path: str) -> Nodo:
    node = root
    for ch in path:
        if node is None:
            return None
        if ch.upper() == 'L':
            node = node.left
        elif ch.upper() == 'R':
            node = node.right
        else:
            return None
    return node


# Evalúa recursivamente el árbol lógico considerando la posible inserción
# de un único Flip-Flop SR en cualquier nodo (entrada o salida)
# ff_map almacena la ubicación del flip-flop y si está en 'input' o 'output'
def evaluate_with_flipflop(node: Nodo, ff_map: dict, path: str = ""):
    if node.is_leaf():
        val = int(node.value)

        # Si existe un flip-flop en la entrada de esta hoja, se procesa antes de devolver el valor
        if path in ff_map and ff_map[path][1] == 'input':
            ff = ff_map[path][0]
            out = ff.operar(val, 0)
            val = out[0] if isinstance(out, tuple) else int(out)

        node.result = val
        return val

    # Evaluación recursiva de los subárboles izquierdo y derecho
    left_val = evaluate_with_flipflop(node.left, ff_map, path + 'L')
    right_val = evaluate_with_flipflop(node.right, ff_map, path + 'R')

    # Si hay un flip-flop en la entrada del nodo actual, procesa antes de la compuerta
    if path in ff_map and ff_map[path][1] == 'input':
        ff = ff_map[path][0]
        out = ff.operar(left_val, right_val)
        if isinstance(out, tuple):
            left_val = right_val = out[0]
        else:
            left_val = right_val = int(out)

    # Se ejecuta la compuerta lógica asociada al nodo
    gate_out = node.gate.operar(int(left_val), int(right_val))

    # Si hay un flip-flop en la salida del nodo, se procesa después de la compuerta
    if path in ff_map and ff_map[path][1] == 'output':
        ff = ff_map[path][0]
        out = ff.operar(int(gate_out), 0)
        gate_out = out[0] if isinstance(out, tuple) else int(out)

    # Se almacena el resultado final en el nodo
    node.result = int(gate_out) if not isinstance(gate_out, tuple) else int(gate_out[0])
    return node.result


# Función principal que controla toda la interacción por consola
# Gestiona la creación del árbol, asignación de entradas, inserción del flip-flop
# y reevaluación dinámica del circuito
def interactive_console():
    print_separator("CIRCUITO LÓGICO - MODO CONSOLA")

    # Solicita al usuario la cantidad de niveles del árbol (máximo 6)
    while True:
        try:
            num_levels = int(input("Ingrese cantidad de niveles de compuertas (1-6): ").strip())
            if 1 <= num_levels <= 6:
                break
        except Exception:
            pass
        print("Valor inválido. Intente nuevamente.")

    # Permite seleccionar el tipo de compuerta para cada nivel
    gate_types = []
    names = list(GATE_MAP.keys())
    for i in range(1, num_levels + 1):
        while True:
            print(f"Nivel {i} - opciones: {', '.join(names)}")
            choice = input(f"Elija compuerta para nivel {i} (por defecto AND): ").strip().upper() or 'AND'
            if choice in GATE_MAP:
                gate_types.append(GATE_MAP[choice])
                break
            print("Opción inválida. Intente nuevamente.")

    # Construye el árbol lógico utilizando el TreeBuilder
    builder = TreeBuilder(num_levels=num_levels, gate_types=gate_types)
    root = builder.build()
    stats = builder.get_statistics()

    print_separator("Árbol construido")
    print("Estadísticas:")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    # Solicita los valores de las hojas (entradas del circuito)
    total_leaves = stats['total_leaves']
    print(f"\nHay {total_leaves} entradas (hojas). Ingrese valores separados por espacio (0/1).")

    vals = None
    while True:
        s = input(f"Ingrese {total_leaves} valores (o 'r' aleatorio, vacío = todos 0): ").strip()
        if s.lower() == 'r':
            import random
            vals = [random.randint(0,1) for _ in range(total_leaves)]
            break
        if s == '':
            vals = [0]*total_leaves
            break
        parts = s.split()
        if len(parts) == total_leaves and all(p in ('0','1') for p in parts):
            vals = [int(p) for p in parts]
            break
        print("Entrada inválida. Asegúrese de poner exactamente los valores requeridos.")

    # Asigna los valores ingresados a las hojas del árbol
    leaves = builder.get_leaves()
    for i, v in enumerate(vals):
        leaves[i].value = int(v)

    print_separator("Entradas asignadas")
    for i, v in enumerate(vals):
        print(f"  Entrada {i}: {v}")

    # Permite agregar opcionalmente un único Flip-Flop SR
    ff_map = {}
    add_ff = input("Desea agregar un FlipFlop SR en alguna entrada/salida? (s/N): ").strip().lower() == 's'

    if add_ff:
        print("Indique la posición del nodo donde colocar el FlipFlop.")
        print("Use ruta desde la raíz con L/R (ej: ''=raiz, L=izq, RL=der-izq).")

        path = input("Ruta del nodo: ").strip().upper()
        pos = ''

        while pos not in ('INPUT','OUTPUT'):
            pos = input("Posición del FlipFlop ('input' o 'output'): ").strip().upper()

        target = get_node_by_path(root, path) if path != '' else root

        if target is None:
            print("Ruta inválida. No se agregó FlipFlop.")
        else:
            ff = FlipFlop()
            ff_map[path] = (ff, 'input' if pos=='INPUT' else 'output')
            print(f"FlipFlop agregado en ruta '{path}' como {pos}.")

    # Evalúa el circuito completo y muestra el resultado
    evaluate_with_flipflop(root, ff_map, path='')
    print_separator("Resultado del circuito")
    print_tree(root)
    print(f"\nResultado final (raíz): {root.result}")

    # Bucle interactivo para modificar entradas y reevaluar el circuito
    while True:
        cmd = input("\nComandos: [c]ambiar entradas, [r]e-evaluar, [p]rint árbol, [q] salir: ").strip().lower()

        if cmd == 'q':
            break

        if cmd == 'p':
            print_tree(root)
            continue

        if cmd == 'c':
            s = input(f"Ingrese {total_leaves} valores separados (0/1): ").strip()
            parts = s.split()
            if len(parts) != total_leaves or not all(p in ('0','1') for p in parts):
                print("Entrada inválida")
                continue
            for i, p in enumerate(parts):
                leaves[i].value = int(p)
            print("Entradas actualizadas")
            continue

        if cmd == 'r':
            evaluate_with_flipflop(root, ff_map, path='')
            print_tree(root)
            print(f"Resultado final (raíz): {root.result}")
            continue

        print("Comando no reconocido")


# Punto de entrada del programa cuando se ejecuta directamente el archivo
if __name__ == '__main__':
    try:
        interactive_console()
    except KeyboardInterrupt:
        print("\nSaliendo...")