from tree import TreeBuilder
from gates import AND, OR


def test_treebuilder_counts_and_structure():
    builder = TreeBuilder(num_levels=2, gate_types=[AND, OR])
    root = builder.build()

    stats = builder.get_statistics()
    assert stats["num_levels"] == 2
    assert stats["total_leaves"] == 4
    assert stats["gates_per_level"]["Nivel 1"] == 1
    assert stats["gates_per_level"]["Nivel 2"] == 2

    # Raíz debe ser nodo interno
    assert root.is_internal()
    # Hijos de la raíz deben existir
    assert root.left is not None and root.right is not None


def test_leaves_are_leafs_and_evaluate():
    builder = TreeBuilder(num_levels=2, gate_types=[AND, OR])
    root = builder.build()

    # Obtener hojas desde la estructura creada
    leaves = builder.get_leaves()
    assert len(leaves) == 4

    # Asignar valores a hojas y evaluar
    values = [1, 1, 0, 0]
    for i, v in enumerate(values):
        leaves[i].value = v
        assert leaves[i].is_leaf()

    result = root.evaluate()
    # OR nodes: left OR = 1, right OR = 0 -> root AND(1,0) == 0
    assert result == 0


def test_verify_formula_helper():
    builder = TreeBuilder(num_levels=3, gate_types=[AND, AND, AND])
    root = builder.build()
    stats = builder.get_statistics()
    gates_per_level = [stats['gates_per_level'].get(f"Nivel {i}", 0) for i in range(1, 4)]
    assert TreeBuilder.verify_formula(3, gates_per_level) is True
