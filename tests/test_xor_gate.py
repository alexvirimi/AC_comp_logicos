from gates import XOR


def test_xor_gate_basic():
    g = XOR()
    assert g.operar(0, 0) == 0
    assert g.operar(0, 1) == 1
    assert g.operar(1, 0) == 1
    assert g.operar(1, 1) == 0
