from gates import NOR


def test_nor_gate_basic():
    g = NOR()
    assert g.operar(0, 0) == 1
    assert g.operar(0, 1) == 0
    assert g.operar(1, 0) == 0
    assert g.operar(1, 1) == 0
