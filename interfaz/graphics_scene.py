from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtCore import Qt
from logica.compuertas import get_gates_per_level
from .graphics_items import InputNodeItem, GateItem, WireItem


class CircuitScene(QGraphicsScene):
    def __init__(self, circuit):
        super().__init__()
        self.circuit = circuit
        self.inputs_items = []
        self.gate_items = []
        self.wires = []
        self.setBackgroundBrush(Qt.GlobalColor.black)
        self.build_scene()

    def build_scene(self):
        self.clear()
        self.inputs_items.clear()
        self.gate_items.clear()
        self.wires.clear()

        levels = self.circuit.levels
        width_spacing = 200
        height_spacing = 80

        # Crear inputs
        for i in range(self.circuit.input_count):
            x = 0
            y = i * height_spacing
            item = InputNodeItem(i, x, y)
            self.addItem(item)
            self.inputs_items.append(item)

        # Crear niveles
        previous_nodes = self.inputs_items

        for level in range(levels):
            gate_count = get_gates_per_level(level, levels)
            level_items = []
            x = (level + 1) * width_spacing

            for i in range(gate_count):
                y = i * height_spacing * (2 ** level)
                gate_type = self.circuit.gate_types[level]
                gate = GateItem(x, y, gate_type)
                self.addItem(gate)
                level_items.append(gate)

                # Conectar wires
                if previous_nodes:
                    a = previous_nodes[i * 2]
                    b = previous_nodes[i * 2 + 1]

                    wire1 = WireItem(a.x(), a.y(), gate.x(), gate.y() - 10)
                    wire2 = WireItem(b.x(), b.y(), gate.x(), gate.y() + 10)

                    self.addItem(wire1)
                    self.addItem(wire2)

                    self.wires.append((wire1, level, i, 0))
                    self.wires.append((wire2, level, i, 1))

            previous_nodes = level_items
            self.gate_items.append(level_items)

        self.update_signals()

    def update_signals(self):
        results = self.circuit.compute()

        # Actualizar gates
        for level, gates in enumerate(self.gate_items):
            for i, gate in enumerate(gates):
                if level < len(results) and i < len(results[level]):
                    gate.set_output(results[level][i])

        # Actualizar wires
        for wire, level, gate_index, input_index in self.wires:
            if level == 0:
                value = self.inputs_items[gate_index * 2 + input_index].value
            else:
                value = results[level - 1][gate_index * 2 + input_index]
            wire.set_signal(value)