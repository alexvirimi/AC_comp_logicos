from gates import AND


def test_and_gate_basic():
    g = AND()
    assert g.operar(0, 0) == 0
    assert g.operar(0, 1) == 0
    assert g.operar(1, 0) == 0
    assert g.operar(1, 1) == 1
