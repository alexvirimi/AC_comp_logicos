#node.py
#Este módulo define la estructura fundamental del árbol lógico del proyecto mediante la clase Nodo, 
#que representa cada elemento del circuito.
#Un nodo puede ser una compuerta interna con dos hijos o una hoja que almacena un valor de entrada (0 o 1).
#Su función principal dentro del sistema es modelar la estructura del circuito como un árbol binario perfecto
#y permitir su evaluación recursiva para obtener el resultado final del circuito lógico.

from gates.base import Compuerta
from typing import Optional, Union, Tuple

class Nodo:
    def __init__(
        self,
        gate: Optional[Compuerta] = None,
        left: Optional['Nodo'] = None,
        right: Optional['Nodo'] = None,
        value: Optional[int] = None
    ):
        """
        Args:
            gate: Instancia de Compuerta (None si es hoja)
            left: Nodo hijo izquierdo (None si es hoja)
            right: Nodo hijo derecho (None si es hoja)
            value: Valor (0 o 1) si es nodo hoja, None si es interno
        """
        self.gate = gate
        self.left = left
        self.right = right
        self.value = value
        self.result = None

    def is_leaf(self) -> bool:
        return (
            self.left is None and
            self.right is None and
            self.gate is None and
            self.value is not None
        )

    def is_internal(self) -> bool:
        return (
            self.gate is not None and
            self.left is not None and
            self.right is not None
        )

    def evaluate(self) -> Union[int, Tuple[int, int]]:
        if not (self.is_leaf() or self.is_internal()):
            raise ValueError("Nodo malformado: no es hoja ni nodo interno")

        if self.is_leaf():
            # Si hay un FlipFlop adjunto al nodo, usarlo como envoltura sobre la
            # salida de la hoja. El FlipFlop espera (Set, Reset) como entradas.
            if hasattr(self, 'attached_flipflop') and self.attached_flipflop is not None:
                reset_val = getattr(self, 'flip_reset_value', 0)
                ff_out = self.attached_flipflop.operar(self.value, reset_val)
                # FlipFlop puede retornar tuple (Q, Q_negado)
                if isinstance(ff_out, tuple):
                    self.result = ff_out[0]
                else:
                    self.result = ff_out
                return self.result

            self.result = self.value
            return self.value

        left_result = self.left.evaluate()
        right_result = self.right.evaluate()

        gate_result = self.gate.operar(left_result, right_result)

        # Aplicar FlipFlop adjunto al nodo interno (si existe). Esto permite
        # insertar un FlipFlop en la salida de cualquier compuerta/interior.
        if isinstance(gate_result, tuple):
            current = gate_result[0]
        else:
            current = gate_result

        if hasattr(self, 'attached_flipflop') and self.attached_flipflop is not None:
            reset_val = getattr(self, 'flip_reset_value', 0)
            ff_out = self.attached_flipflop.operar(current, reset_val)
            if isinstance(ff_out, tuple):
                self.result = ff_out[0]
            else:
                self.result = ff_out
        else:
            self.result = current

        return self.result

    def __repr__(self) -> str:
        if self.is_leaf():
            return f"Nodo(hoja={self.value})"
        else:
            gate_name = self.gate.__class__.__name__ if self.gate else "None"
            return f"Nodo({gate_name}, resultado={self.result})"