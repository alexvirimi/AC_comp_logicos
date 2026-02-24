import pytest

from gates.flipflop import FlipFlop
from tree.builder import TreeBuilder
from gates import AND, OR


def test_flipflop_set_and_reset():
    ff = FlipFlop()

    # Inicial
    assert ff.value == 0

    # Set
    out = ff.operar(1, 0)
    assert isinstance(out, tuple)
    assert out[0] == 1
    assert ff.value == 1

    # Reset
    out = ff.operar(0, 1)
    assert out[0] == 0
    assert ff.value == 0


def test_flipflop_set_set_treated_as_set():
    ff = FlipFlop()
    out = ff.operar(1, 1)
    # Por especificación del curso, (1,1) se trata como Set
    assert out[0] == 1
    assert ff.value == 1


def test_flipflop_hold_on_zero_zero():
    ff = FlipFlop()
    ff.operar(1, 0)  # set a 1
    prev = ff.value
    out = ff.operar(0, 0)  # hold
    assert out[0] == prev
    assert ff.value == prev


def test_treebuilder_and_evaluation():
    # Construir árbol de 2 niveles: nivel1 AND, nivel2 OR (homogéneo por nivel)
    builder = TreeBuilder(num_levels=2, gate_types=[AND, OR])
    root = builder.build()

    # Obtener hojas creadas
    leaves = builder.get_leaves()
    assert len(leaves) == 4

    # Asignar valores: [1,1,0,0]
    leaves[0].value = 1
    leaves[1].value = 1
    leaves[2].value = 0
    leaves[3].value = 0

    # Evaluar: OR nodes -> (1, 0), root AND(1,0) -> 0
    result = root.evaluate()
    assert result == 0


def test_verify_formula_helper():
    # Verificar que la fórmula compuertas por nivel se cumple
    builder = TreeBuilder(num_levels=3, gate_types=[AND, AND, AND])
    root = builder.build()
    stats = builder.get_statistics()
    gates_per_level = [stats['gates_per_level'].get(f"Nivel {i}", 0) for i in range(1, 4)]
    assert TreeBuilder.verify_formula(3, gates_per_level) is True
