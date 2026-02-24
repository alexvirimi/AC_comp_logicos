from gates import OR


def test_or_gate_basic():
    g = OR()
    assert g.operar(0, 0) == 0
    assert g.operar(0, 1) == 1
    assert g.operar(1, 0) == 1
    assert g.operar(1, 1) == 1
