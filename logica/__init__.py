"""
Paquete logica - Contiene toda la lógica de compuertas y circuitos
"""

from .compuertas import evaluate_gate, get_input_count, get_gates_per_level
from .circuito import Circuit

__all__ = ['evaluate_gate', 'get_input_count', 'get_gates_per_level', 'Circuit']
