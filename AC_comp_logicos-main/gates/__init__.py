"""Módulo de compuertas lógicas."""

from gates.base import Compuerta
from gates.and_gate import AND
from gates.or_gate import OR
from gates.nand_gate import NAND
from gates.nor_gate import NOR
from gates.xor_gate import XOR
from gates.flipflop import FlipFlop

__all__ = [
    'Compuerta',
    'AND',
    'OR',
    'NAND',
    'NOR',
    'XOR',
    'FlipFlop',
]
