#Este módulo implementa la clase TreeBuilder, encargada de construir automáticamente 
#el árbol binario perfecto que representa el circuito lógico del proyecto.
#Su función es generar la estructura completa del circuito a partir de la cantidad de niveles 
#de compuertas (máximo 6) y los tipos de compuertas definidos para cada nivel, 
#asegurando que todas las compuertas de un mismo nivel sean homogéneas 
#y que se cumpla la fórmula teórica de cantidad de nodos por nivel.
#Además, permite obtener estadísticas estructurales del árbol y verificar que
#la construcción respete la relación matemática esperada. (TENGO SUEÑOOOOOOOOOOOOOOOOOOOOO)


from tree.node import Nodo
from gates.base import Compuerta
from typing import List, Type


class TreeBuilder:
    def __init__(self, num_levels: int, gate_types: List[Type[Compuerta]]):
        """
        Args:
            num_levels: Cantidad de niveles de compuertas (máximo 6)
            gate_types: Lista de tipos de compuertas por nivel
                        Ejemplo: [AND, OR, NAND] para 3 niveles
        Raises:
            ValueError: Si num_levels > 6 o len(gate_types) != num_levels
        """
        if num_levels > 6:
            raise ValueError("Máximo 6 niveles de compuertas permitidos")
        if num_levels < 1:
            raise ValueError("Mínimo 1 nivel de compuertas")
        if len(gate_types) != num_levels:
            raise ValueError(
                f"Se esperan {num_levels} tipos de compuertas, "
                f"se recibieron {len(gate_types)}"
            )

        self.num_levels = num_levels
        self.gate_types = gate_types
        self._nodes_by_level = {}

    def build(self) -> Nodo:
        total_leaves = 2 ** self.num_levels
        leaves = [Nodo(value=0) for _ in range(total_leaves)]
        self._nodes_by_level[self.num_levels] = leaves

        current_level_nodes = leaves

        for level_idx in range(self.num_levels - 1, -1, -1):
            gate_class = self.gate_types[level_idx]
            next_level_nodes = []

            for i in range(0, len(current_level_nodes), 2):
                left_child = current_level_nodes[i]
                right_child = current_level_nodes[i + 1]

                gate = gate_class()
                internal_node = Nodo(
                    gate=gate,
                    left=left_child,
                    right=right_child
                )
                next_level_nodes.append(internal_node)

            actual_level = level_idx + 1
            self._nodes_by_level[actual_level] = next_level_nodes
            current_level_nodes = next_level_nodes

        root = current_level_nodes[0]
        return root

    def get_statistics(self) -> dict:
        if not self._nodes_by_level:
            raise ValueError("Primero debe llamar a build()")

        gates_per_level = {}
        total_gates = 0

        for level in range(1, self.num_levels + 1):
            count = len(self._nodes_by_level.get(level, []))
            if count > 0:
                gates_per_level[f"Nivel {level}"] = count
                total_gates += count

        return {
            "num_levels": self.num_levels,
            "total_gates": total_gates,
            "total_leaves": 2 ** self.num_levels,
            "gates_per_level": gates_per_level
        }

    @staticmethod
    def verify_formula(num_levels: int, gates_per_level: List[int]) -> bool:
        """
        Args:
            num_levels: Cantidad de niveles
            gates_per_level: Lista de cantidades reales por nivel
        Returns:
            True si cumple la fórmula, False si no
        """
        for level in range(1, num_levels + 1):
            expected = 2 ** (level - 1)
            actual = gates_per_level[level - 1]
            if actual != expected:
                return False
        return True