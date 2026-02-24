import pytest

from gates import AND, OR, NAND, NOR, XOR


def test_and_gate():
    g = AND()
    assert g.operar(0, 0) == 0
    assert g.operar(0, 1) == 0
    assert g.operar(1, 0) == 0
    assert g.operar(1, 1) == 1


def test_or_gate():
    g = OR()
    assert g.operar(0, 0) == 0
    assert g.operar(0, 1) == 1
    assert g.operar(1, 0) == 1
    assert g.operar(1, 1) == 1


def test_nand_gate():
    g = NAND()
    assert g.operar(0, 0) == 1
    assert g.operar(0, 1) == 1
    assert g.operar(1, 0) == 1
    assert g.operar(1, 1) == 0


def test_nor_gate():
    g = NOR()
    assert g.operar(0, 0) == 1
    assert g.operar(0, 1) == 0
    assert g.operar(1, 0) == 0
    assert g.operar(1, 1) == 0


def test_xor_gate():
    g = XOR()
    assert g.operar(0, 0) == 0
    assert g.operar(0, 1) == 1
    assert g.operar(1, 0) == 1
    assert g.operar(1, 1) == 0
