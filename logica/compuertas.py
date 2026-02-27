"""Definición de compuertas lógicas y sus operaciones."""

from typing import Literal

GateType = Literal["AND", "OR", "NAND", "NOR", "XOR", "XNOR"]

AVAILABLE_GATES = ["AND", "OR", "NAND", "NOR", "XOR", "XNOR"]

def evaluate_gate(gate: GateType, a: int, b: int) -> int:
    """Evalúa una compuerta lógica con dos entradas.
    
    Args:
        gate: Tipo de compuerta
        a, b: Valores de entrada (0 o 1)
    
    Returns:
        Resultado de la operación (0 o 1)
    """
    a, b = int(a), int(b)
    
    if gate == "AND":
        return a & b
    elif gate == "OR":
        return a | b
    elif gate == "NAND":
        return (a & b) ^ 1
    elif gate == "NOR":
        return (a | b) ^ 1
    elif gate == "XOR":
        return a ^ b
    elif gate == "XNOR":
        return (a ^ b) ^ 1
    return 0

def get_gates_per_level(level: int, total_levels: int) -> int:
    """Calcula la cantidad de compuertas en un nivel.

    En el nivel 0 (el más cercano a las entradas) debe haber la mitad
    de las entradas, es decir 2**(total_levels-1). A medida que avanzamos
    un nivel, la cantidad se divide en dos. Por eso restamos 1 al nivel.
    """
    # por ejemplo: total_levels=4 -> niveles 0..3
    # nivel 0 -> 2**(4-1)=8, nivel 1 -> 4, nivel 2 -> 2, nivel3 ->1
    return 2 ** (total_levels - level - 1)

def get_input_count(total_levels: int) -> int:
    """Calcula cantidad de entradas necesarias."""
    return 2 ** total_levels
