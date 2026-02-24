from gates import NAND


def test_nand_gate_basic():
    g = NAND()
    assert g.operar(0, 0) == 1
    assert g.operar(0, 1) == 1
    assert g.operar(1, 0) == 1
    assert g.operar(1, 1) == 0
