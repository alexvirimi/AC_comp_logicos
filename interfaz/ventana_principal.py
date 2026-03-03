"""Ventana principal con SVG reales para compuertas - Posicionamiento absoluto."""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtSvgWidgets import QSvgWidget

from logica.circuito import Circuit
from logica.compuertas import get_gates_per_level
from recursos.constantes import COLORS, LEVEL_COLORS
from .wire_overlay import WireOverlay


# Constantes de tamaño
INPUT_WIDTH = 100
INPUT_HEIGHT = 80
GATE_WIDTH = 140
GATE_HEIGHT = 80
HEADER_HEIGHT = 60
COLUMN_SPACING = 40


# =========================
# COLUMNA DE ENTRADAS (SVG)
# =========================
class InputsColumn(QFrame):
    """Columna de entradas con posiciones calculadas matemáticamente."""

    input_changed = pyqtSignal(int, int)

    def __init__(self, circuit: Circuit):
        super().__init__()
        self.circuit = circuit
        self.input_buttons = []  # (container, label)
        self._init_ui()

    def _init_ui(self):
        self.setFixedWidth(INPUT_WIDTH)
        self._create_children()
        self._layout_children()

    def _create_children(self):
        """Crea los contenedores para cada entrada."""
        for i in range(len(self.circuit.inputs)):
            container = QFrame(self)
            container.setFixedSize(INPUT_WIDTH, INPUT_HEIGHT)

            # Layout interno para centrar SVG y label
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            svg = QSvgWidget("input.svg", container)
            svg.setFixedSize(40, 40)

            label = QLabel("0", container)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(f"color: {COLORS['red']}; font-weight: bold;")

            layout.addWidget(svg, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)

            container.mousePressEvent = lambda event, idx=i: self._toggle(idx)

            self.input_buttons.append((container, label))

    def _layout_children(self):
        """Posiciona cada contenedor usando fórmula y = spacing/2 + i*spacing."""
        n = len(self.input_buttons)
        total_height = n * INPUT_HEIGHT
        self.setFixedHeight(total_height)

        spacing = total_height / n
        for i, (container, _) in enumerate(self.input_buttons):
            center_y = spacing / 2 + i * spacing
            y = int(center_y - INPUT_HEIGHT / 2)
            container.move(0, y)

    def _toggle(self, index):
        value = 0 if self.circuit.inputs[index] else 1
        self.circuit.set_input(index, value)

        _, label = self.input_buttons[index]
        color = COLORS['green'] if value else COLORS['red']
        label.setText(str(value))
        label.setStyleSheet(f"color: {color}; font-weight: bold;")

        self.input_changed.emit(index, value)


# =========================
# COLUMNA DE NIVEL (SVG)
# =========================
class LevelColumn(QFrame):
    """Columna de un nivel de compuertas con posiciones absolutas."""

    gate_changed = pyqtSignal(int, str)

    def __init__(self, circuit: Circuit, level: int, color_dict: dict):
        super().__init__()
        self.circuit = circuit
        self.level = level
        self.color_dict = color_dict
        self.gates_per_level = get_gates_per_level(level, circuit.levels)
        self.gate_widgets = []  # (svg, label)
        self.header = None
        self._init_ui()

    def _init_ui(self):
        self.setFixedWidth(GATE_WIDTH)
        self._create_header()
        self._create_gates()
        self._layout_children()

    def _create_header(self):
        """Crea el header con título y combo."""
        self.header = QFrame(self)
        self.header.setFixedSize(GATE_WIDTH, HEADER_HEIGHT)

        layout = QHBoxLayout(self.header)
        layout.setContentsMargins(5, 0, 5, 0)

        title = QLabel(f"L{self.level}", self.header)
        title.setStyleSheet(f"color: {self.color_dict['text']}; font-weight: bold;")

        combo = QComboBox(self.header)
        combo.addItems(["AND", "OR", "NAND", "NOR", "XOR", "XNOR"])
        combo.setCurrentText(self.circuit.gate_types[self.level])
        combo.currentTextChanged.connect(self._on_gate_changed)

        layout.addWidget(title)
        layout.addWidget(combo)
        layout.addStretch()

    def _create_gates(self):
        """Crea los contenedores para cada compuerta del nivel."""
        for _ in range(self.gates_per_level):
            container = QFrame(self)
            container.setFixedSize(GATE_WIDTH, GATE_HEIGHT)

            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            gate_type = self.circuit.gate_types[self.level]
            svg = QSvgWidget(f"{gate_type.lower()}.svg", container)
            svg.setFixedSize(70, 70)

            output_label = QLabel("0", container)
            output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            output_label.setStyleSheet(f"color: {COLORS['red']}; font-weight: bold;")

            layout.addWidget(svg, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(output_label)

            self.gate_widgets.append((svg, output_label))

    def _layout_children(self):
        """Posiciona header y compuertas con cálculo exacto."""
        n = self.gates_per_level
        gates_height = n * GATE_HEIGHT
        total_height = HEADER_HEIGHT + gates_height
        self.setFixedHeight(total_height)

        # Header arriba
        self.header.move(0, 0)

        # Compuertas debajo del header
        spacing = gates_height / n
        for i, (svg, _) in enumerate(self.gate_widgets):
            container = svg.parent()
            center_y = HEADER_HEIGHT + spacing / 2 + i * spacing
            y = int(center_y - GATE_HEIGHT / 2)
            container.move(0, y)

    def _on_gate_changed(self, gate_type):
        self.circuit.set_gate_type(self.level, gate_type)

        for svg, _ in self.gate_widgets:
            svg.load(f"{gate_type.lower()}.svg")

        self.gate_changed.emit(self.level, gate_type)

    def update_display(self, results):
        for i, (_, label) in enumerate(self.gate_widgets):
            if i < len(results):
                val = results[i]
                color = COLORS['green'] if val else COLORS['red']
                label.setText(str(val))
                label.setStyleSheet(f"color: {color}; font-weight: bold;")


# =========================
# VENTANA PRINCIPAL
# =========================
class CircuitWindow(QMainWindow):
    """Ventana principal que integra columnas y overlay de cables."""

    def __init__(self, levels):
        super().__init__()

        self.setWindowTitle("Diseñador Profesional de Circuitos")
        self.setGeometry(100, 100, 1600, 900)

        self.circuit = Circuit(levels)

        self._init_ui()
        self._update_display()

    def _init_ui(self):
        central = QWidget()
        main_layout = QVBoxLayout()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        scroll_layout = QHBoxLayout()
        scroll_layout.setSpacing(COLUMN_SPACING)
        scroll_layout.setContentsMargins(20, 20, 20, 20)

        # Columna de entradas
        self.inputs_column = InputsColumn(self.circuit)
        self.inputs_column.input_changed.connect(self._update_display)
        scroll_layout.addWidget(self.inputs_column)

        # Columnas de niveles
        self.level_columns = []
        for level in range(self.circuit.levels):
            col = LevelColumn(
                self.circuit,
                level,
                LEVEL_COLORS[level % len(LEVEL_COLORS)]
            )
            col.gate_changed.connect(self._update_display)
            scroll_layout.addWidget(col)
            self.level_columns.append(col)

        scroll_layout.addStretch()
        self.scroll_widget.setLayout(scroll_layout)

        # Calcular tamaño total del contenido para el scroll
        self._resize_scroll_content()

        self.scroll.setWidget(self.scroll_widget)
        main_layout.addWidget(self.scroll)
        central.setLayout(main_layout)
        self.setCentralWidget(central)

        # Overlay de cables
        self.overlay = WireOverlay(
            self.scroll_widget,
            self.circuit,
            self.inputs_column,
            self.level_columns,
            self.scroll
        )
        self.overlay.resize(self.scroll_widget.size())
        self.overlay.raise_()

    def _resize_scroll_content(self):
        """Ajusta el tamaño del scroll_widget al contenido total."""
        # Ancho total: suma de anchos de columnas + espaciados
        total_width = (self.inputs_column.width() +
                       sum(col.width() for col in self.level_columns) +
                       COLUMN_SPACING * (len(self.level_columns) + 1))

        # Alto máximo entre todas las columnas
        max_height = max(
            self.inputs_column.height(),
            max((col.height() for col in self.level_columns), default=0)
        )

        self.scroll_widget.setFixedSize(total_width, max_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.overlay.resize(self.scroll_widget.size())
        self.overlay.update()

    def _update_display(self):
        results = self.circuit.compute()

        for level, col in enumerate(self.level_columns):
            if level < len(results):
                col.update_display(results[level])

        self.overlay.update()