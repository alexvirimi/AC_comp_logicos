"""Lógica del circuito de compuertas."""

from typing import List
from .compuertas import GateType, evaluate_gate, get_input_count


class Circuit:
    """Representa un circuito de compuertas lógicas."""
    
    def __init__(self, levels: int, gate_types: List[GateType] | None = None, inputs: List[int] | None = None):
        """Inicializa el circuito."""
        self.levels = levels
        self.input_count = get_input_count(levels)
        
        if gate_types is None:
            self.gate_types = ["AND"] * levels
        else:
            self.gate_types = gate_types[:levels]
        
        if inputs is None:
            self.inputs = [0] * self.input_count
        else:
            self.inputs = [int(v) for v in inputs[:self.input_count]]
        
        self.results: List[List[int]] = []
    
    def set_input(self, index: int, value: int) -> None:
        """Establece el valor de una entrada."""
        if 0 <= index < self.input_count:
            self.inputs[index] = int(value) & 1
    
    def set_gate_type(self, level: int, gate_type: GateType) -> None:
        """Cambia el tipo de compuerta de un nivel."""
        if 0 <= level < self.levels:
            self.gate_types[level] = gate_type
    
    def compute(self) -> List[List[int]]:
        """Calcula el resultado del circuito."""
        self.results = []
        current_inputs = self.inputs[:]
        
        for level in range(self.levels):
            gate_type = self.gate_types[level]
            level_results = []
            
            for i in range(0, len(current_inputs), 2):
                a = current_inputs[i] if i < len(current_inputs) else 0
                b = current_inputs[i + 1] if i + 1 < len(current_inputs) else 0
                result = evaluate_gate(gate_type, a, b)
                level_results.append(result)
            
            self.results.append(level_results)
            current_inputs = level_results
        
        return self.results
    
    def get_final_output(self) -> int:
        """Retorna la salida final del circuito."""
        if self.results and self.results[-1]:
            return self.results[-1][0]
        return 0
    
    def reset(self) -> None:
        """Reinicia el circuito al estado inicial.

        - Todas las entradas en 0.
        - Resultados vacíos.
        - Tipos de compuerta regresan a AND.
        """
        self.inputs = [0] * self.input_count
        self.results = []
        # Restaurar tipos de compuerta a AND en todos los niveles
        self.gate_types = ["AND"] * self.levels
