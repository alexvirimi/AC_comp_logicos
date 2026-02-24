#Le dije a gepete que me hiciera un main de prueba pa ver si aja, la implementacion de los arboles salio bien

from gates import AND, OR, NAND, NOR, XOR, FlipFlop
from tree.node import Nodo
from tree.builder import TreeBuilder


def print_separator(title: str = ""):
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print("-" * 60)


def print_tree_structure(node: Nodo, level: int = 0, prefix: str = ""):
    if node is None:
        return

    if node.is_leaf():
        symbol = f"Hoja [valor={node.value}]"
    else:
        gate_name = node.gate.__class__.__name__
        result = node.result if node.result is not None else "?"
        symbol = f"{gate_name} [resultado={result}]"

    print(f"{prefix}{symbol}")

    if node.left is not None or node.right is not None:
        if node.left is not None:
            print_tree_structure(node.left, level + 1, prefix + "  ├─ ")
        if node.right is not None:
            print_tree_structure(node.right, level + 1, prefix + "  └─ ")


def assign_values_to_leaves(node: Nodo, values: list, index: list = None):
    """
    Args:
        node: Nodo actual
        values: Lista de valores a asignar
        index: Índice actual (usa lista para pasar por referencia)
    """
    if index is None:
        index = [0]

    if node is None:
        return

    if node.left is not None:
        assign_values_to_leaves(node.left, values, index)

    if node.is_leaf():
        if index[0] < len(values):
            node.value = values[index[0]]
            index[0] += 1

    if node.right is not None:
        assign_values_to_leaves(node.right, values, index)


def print_leaf_values(node: Nodo, values: list = None, index: list = None):
    """
    Args:
        node: Nodo actual
        values: Lista acumuladora de valores
        index: Índice actual
    """
    if values is None:
        values = []
    if index is None:
        index = [0]

    if node is None:
        return values

    if node.left is not None:
        print_leaf_values(node.left, values, index)

    if node.is_leaf():
        values.append(node.value)
        print(f"  Entrada {index[0]}: {node.value}")
        index[0] += 1

    if node.right is not None:
        print_leaf_values(node.right, values, index)

    return values


def test_simple_tree():
    print_separator("PRUEBA 1: Árbol de 2 Niveles (AND en nivel 1, OR en nivel 2)")

    builder = TreeBuilder(num_levels=2, gate_types=[AND, OR])
    root = builder.build()

    stats = builder.get_statistics()
    print("Estadísticas:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\nAsignando valores a las entradas...")
    values = [0, 1, 0, 1]
    assign_values_to_leaves(root, values)

    print("\nValores asignados:")
    print_leaf_values(root)

    print("\nEvaluando circuito...")
    result = root.evaluate()
    print(f"  Resultado final: {result}")

    print("\nEstructura del árbol después de evaluación:")
    print_tree_structure(root)


def test_larger_tree():
    print_separator("PRUEBA 2: Árbol de 3 Niveles (AND → OR → NAND)")

    builder = TreeBuilder(num_levels=3, gate_types=[AND, OR, NAND])
    root = builder.build()

    stats = builder.get_statistics()
    print("Estadísticas:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\nAsignando valores a las entradas (todos 1s)...")
    values = [1, 1, 1, 1, 1, 1, 1, 1]
    assign_values_to_leaves(root, values)

    print("\nValores asignados:")
    print_leaf_values(root)

    print("\nEvaluando circuito...")
    result = root.evaluate()
    print(f"  Resultado final: {result}")

    print("\nEstructura del árbol después de evaluación:")
    print_tree_structure(root)


def test_verify_formula():
    print_separator("PRUEBA 3: Verificación de Fórmula")

    for num_levels in range(1, 4):
        builder = TreeBuilder(
            num_levels=num_levels,
            gate_types=[AND] * num_levels
        )
        root = builder.build()
        stats = builder.get_statistics()

        gates_per_level = [
            stats["gates_per_level"].get(f"Nivel {i}", 0)
            for i in range(1, num_levels + 1)
        ]

        is_valid = TreeBuilder.verify_formula(num_levels, gates_per_level)

        print(f"\nNiveles: {num_levels}")
        print(f"  Compuertas por nivel: {gates_per_level}")
        print("  Fórmula válida" if is_valid else "  Fórmula inválida")
        print(f"  Total de entradas: {stats['total_leaves']}")


def test_max_levels():
    print_separator("PRUEBA 4: Árbol Máximo (6 Niveles)")

    builder = TreeBuilder(
        num_levels=6,
        gate_types=[AND, OR, NAND, NOR, XOR, AND]
    )
    root = builder.build()

    stats = builder.get_statistics()
    print("Estadísticas:")
    print(f"  Niveles: {stats['num_levels']}")
    print(f"  Total de compuertas: {stats['total_gates']}")
    print(f"  Total de entradas: {stats['total_leaves']}")

    import random
    values = [random.randint(0, 1) for _ in range(stats['total_leaves'])]
    assign_values_to_leaves(root, values)

    print("\nValores asignados (primeros 10):")
    first_values = values[:10]
    for i, v in enumerate(first_values):
        print(f"  Entrada {i}: {v}")
    if len(values) > 10:
        print(f"  ... y {len(values) - 10} más")

    print("\nEvaluando circuito...")
    result = root.evaluate()
    print(f"  Resultado final: {result}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  PRUEBAS ESTRUCTURALES - CIRCUITO LÓGICO")
    print("="*60)

    try:
        test_simple_tree()
        test_larger_tree()
        test_verify_formula()
        test_max_levels()

        print_separator("TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")

    except Exception as e:
        print_separator("ERROR DURANTE LAS PRUEBAS")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()