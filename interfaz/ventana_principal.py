from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
import os

try:
    from PyQt6.QtSvgWidgets import QSvgWidget
except ImportError:
    QSvgWidget = None

from logica.circuito import Circuit
from logica.compuertas import get_gates_per_level
from recursos.constantes import COLORS, LEVEL_COLORS


class InputsColumn(QFrame):
    """Columna con botones para togglear las entradas."""
    
    input_changed = pyqtSignal(int, int)  # index, value
    
    def __init__(self, circuit: Circuit):
        super().__init__()
        self.circuit = circuit
        self.input_buttons = []
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_secondary']};
                border-right: 2px solid {COLORS['border_color']};
                padding: 10px;
            }}
        """)
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        title = QLabel("Entradas")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(10)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        main_layout.addWidget(title)
        
        # Add spacing to align with LevelColumn header/info area
        # (accounts for level label + header layout + info label in LevelColumn)
        main_layout.addSpacing(60)
        
        # Get number of gates in level 0 to align inputs
        gates_level_0 = get_gates_per_level(0, self.circuit.levels)
        num_inputs_per_gate = 2  # cada compuerta tiene 2 entradas
        total_inputs = len(self.circuit.inputs)
        
        # Create a grid of input pairs, one row per gate
        gates_layout = QVBoxLayout()
        gates_layout.setSpacing(6)  # match spacing of gate_frames
        
        for gate_idx in range(gates_level_0):
            # Create a VERTICAL layout for the pair of inputs for this gate
            pair_layout = QVBoxLayout()
            pair_layout.setSpacing(0)  # no spacing between buttons
            pair_layout.setContentsMargins(0, 0, 0, 0)  # no margins
            
            # Two inputs per gate, stacked vertically
            for input_offset in range(num_inputs_per_gate):
                input_idx = gate_idx * num_inputs_per_gate + input_offset
                if input_idx < total_inputs:
                    val = self.circuit.inputs[input_idx]
                    btn = QPushButton(str(val))
                    btn.setFixedSize(30, 30)
                    btn.setCheckable(True)
                    btn.setChecked(bool(val))
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {COLORS['red']};
                            color: white;
                            border: 1px solid {COLORS['red']};
                            border-radius: 15px;
                            font-size: 10px;
                            font-weight: bold;
                        }}
                        QPushButton:checked {{
                            background-color: {COLORS['green']};
                            border: 1px solid {COLORS['green']};
                        }}
                        QPushButton:hover {{
                            opacity: 0.8;
                        }}
                    """)
                    btn.clicked.connect(lambda checked, idx=input_idx: self._toggle_input(idx, checked))
                    pair_layout.addWidget(btn)
                    self.input_buttons.append(btn)
            
            # Center the pair of buttons vertically in the frame
            pair_layout.insertStretch(0, 1)
            pair_layout.addStretch(1)
            
            # Create a container frame to match gate height (80px)
            pair_frame = QFrame()
            pair_frame.setLayout(pair_layout)
            pair_frame.setFixedHeight(80)
            pair_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: transparent;
                }}
            """)
            gates_layout.addWidget(pair_frame)
        
        main_layout.addLayout(gates_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def _toggle_input(self, index: int, checked: bool):
        """Alterna el valor de una entrada."""
        value = 1 if checked else 0
        self.circuit.set_input(index, value)
        # actualizar texto del botón
        btn = self.input_buttons[index]
        btn.setText(str(value))
        self.input_changed.emit(index, value)
    
    def update_display(self):
        """Actualiza la visualización de los botones."""
        for i, btn in enumerate(self.input_buttons):
            val = bool(self.circuit.inputs[i])
            btn.setChecked(val)
            btn.setText("1" if val else "0")


class LevelColumn(QFrame):
    """Columna representando un nivel del circuito."""
    
    gate_changed = pyqtSignal(int, str)  # level, gate_type
    
    def __init__(self, circuit: Circuit, level: int, color_dict: dict):
        super().__init__()
        self.circuit = circuit
        self.level = level
        self.color_dict = color_dict
        self.gates_per_level = get_gates_per_level(level, circuit.levels)
        self.results = []
        
        # Estilo neon
        border_color = color_dict['border']
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_secondary']};
                border: 2px dashed {border_color};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        self._init_ui()
        # after building UI, load the correct gate icons
        self._update_icons()
    
    def _init_ui(self):
        """Inicializa la interfaz."""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header con selector de compuerta
        header = QHBoxLayout()
        
        title = QLabel(f"L{self.level}")
        title_font = QFont()
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {self.color_dict['text']};")
        header.addWidget(title)
        
        # Selector de compuerta
        combo = QComboBox()
        gate_list = ["AND", "OR", "NAND", "NOR", "XOR", "XNOR"]
        combo.addItems(gate_list)
        # add icons to items
        for idx, g in enumerate(gate_list):
            path = self._get_gate_icon_path(g)
            if os.path.exists(path):
                combo.setItemIcon(idx, QIcon(path))
        combo.setCurrentText(self.circuit.gate_types[self.level])
        combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS['bg_primary']};
                color: {COLORS['text_primary']};
                border: 1px solid {self.color_dict['border']};
                border-radius: 4px;
                padding: 5px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {COLORS['bg_primary']};
                color: {COLORS['text_primary']};
                selection-background-color: {self.color_dict['border']};
            }}
        """)
        combo.currentTextChanged.connect(lambda gate: self._on_gate_changed(gate))
        header.addWidget(combo)
        self.combo = combo
        header.addStretch()
        
        layout.addLayout(header)
        
        # Información de cantidad de compuertas
        info = QLabel(f"{self.gates_per_level} compuertas")
        info.setStyleSheet(f"color: {self.color_dict['text']}; font-size: 9px;")
        layout.addWidget(info)
        
        # Gates del nivel (stacked verticalmente)
        gates_layout = QVBoxLayout()
        gates_layout.setSpacing(6)
        self.gate_frames = []
        self.output_labels = []
        self.icon_widgets = []  # svg widget or label
        
        for i in range(self.gates_per_level):
            gate_frame = QFrame()
            gate_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['bg_primary']};
                    border: 1px solid {self.color_dict['border']};
                    border-radius: 6px;
                    padding: 6px;
                }}
            """)
            # make frame taller to fit both icon and output
            gate_frame.setFixedSize(60, 80)
            
            gate_layout = QVBoxLayout()
            gate_layout.setContentsMargins(0, 0, 0, 0)
            gate_layout.setSpacing(0)
            
            # icon for gate type
            if QSvgWidget is not None:
                icon_widget = QSvgWidget()
                icon_widget.setFixedSize(36, 36)
            else:
                icon_widget = QLabel()
                icon_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            gate_layout.addWidget(icon_widget)
            self.icon_widgets.append(icon_widget)
            
            output_label = QLabel("0")
            output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            output_label.setStyleSheet(f"color: {COLORS['red']}; font-size: 14px;")
            output_label.setObjectName(f"output_{i}")
            gate_layout.addWidget(output_label)
            
            gate_frame.setLayout(gate_layout)
            gates_layout.addWidget(gate_frame)
            self.gate_frames.append(gate_frame)
            self.output_labels.append(output_label)
        
        layout.addLayout(gates_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def _on_gate_changed(self, gate_type: str):
        """Cuando cambia el tipo de compuerta."""
        self.circuit.set_gate_type(self.level, gate_type)
        self.gate_changed.emit(self.level, gate_type)
        self._update_icons()
    
    def update_display(self, results: list):
        """Actualiza los resultados mostrados."""
        self.results = results
        
        # Actualizar valores y colores de los gates
        # icon updates not required here since gate type doesn't change
        for i, output_label in enumerate(self.output_labels):
            if i < len(results):
                val = results[i]
                color = COLORS['green'] if val == 1 else COLORS['red']
                output_label.setText(str(val))
                output_label.setStyleSheet(f"color: {color}; font-size: 14px;")

    def _get_gate_icon_path(self, gate_type: str) -> str:
        """Return absolute path to SVG icon for given gate type."""
        name = gate_type.lower()
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
        return os.path.join(base, f"{name}.svg")

    def _update_icons(self):
        """Loads and updates each icon widget based on current gate type."""
        icon_path = self._get_gate_icon_path(self.circuit.gate_types[self.level])
        exists = os.path.exists(icon_path)
        for widget in self.icon_widgets:
            if exists:
                if QSvgWidget is not None and isinstance(widget, QSvgWidget):
                    widget.load(icon_path)
                else:
                    icon = QIcon(icon_path)
                    pix = icon.pixmap(36, 36)
                    widget.setPixmap(pix)
            else:
                # clear
                if QSvgWidget is not None and isinstance(widget, QSvgWidget):
                    widget.load(b"")
                else:
                    widget.clear()


class CircuitWindow(QMainWindow):
    """Ventana principal del circuito."""
    
    rebuild_requested = pyqtSignal()  # señal para solicitar reconstrucción
    
    def __init__(self, levels: int):
        super().__init__()
        self.setWindowTitle("Diseñador de Circuitos Lógicos")
        self.setGeometry(0, 0, 1600, 900)
        
        # Crear circuito
        self.circuit = Circuit(levels)
        
        # Crear UI
        self._init_ui()
        
        # Actualizar visualización inicial
        self._update_display()
    
    def _init_ui(self):
        """Inicializa la interfaz."""
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # ===== HEADER =====
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_secondary']};
                border-bottom: 1px solid {COLORS['border_color']};
                padding: 15px 20px;
            }}
        """)
        header_layout = QHBoxLayout()
        
        title = QLabel("Circuito de Compuertas Lógicas")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        header_layout.addWidget(title)
        # badge de niveles
        levels_label = QLabel(f"{self.circuit.levels} niveles")
        levels_label.setStyleSheet(f"color: {COLORS['text_secondary']}; padding: 2px 6px; border: 1px solid {COLORS['text_secondary']}; border-radius: 4px; font-size: 10px;")
        header_layout.addWidget(levels_label)
        
        # Indicador de salida final
        output_label = QLabel("Salida Final:")
        output_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        header_layout.addWidget(output_label)
        
        self.final_output_display = QLabel("0")
        output_font = QFont()
        output_font.setPointSize(12)
        output_font.setBold(True)
        self.final_output_display.setFont(output_font)
        self.final_output_display.setStyleSheet(f"color: {COLORS['red']}; padding: 5px 15px; background-color: {COLORS['bg_primary']}; border-radius: 4px;")
        header_layout.addWidget(self.final_output_display)
        
        header_layout.addStretch()
        
        # Botón reset
        reset_btn = QPushButton("Reiniciar")
        reset_btn.setMinimumHeight(35)
        reset_btn.setMinimumWidth(120)
        reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary_blue']};
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2563eb;
            }}
        """)
        reset_btn.clicked.connect(self._on_reset)
        header_layout.addWidget(reset_btn)
        
        # Botón reconstruir
        rebuild_btn = QPushButton("Reconstruir")
        rebuild_btn.setMinimumHeight(35)
        rebuild_btn.setMinimumWidth(120)
        rebuild_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #7c3aed;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #6d28d9;
            }}
        """)
        rebuild_btn.clicked.connect(self._on_rebuild)
        header_layout.addWidget(rebuild_btn)
        
        header.setLayout(header_layout)
        main_layout.addWidget(header)
        
        # ===== CONTENIDO PRINCIPAL =====
        content = QWidget()
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {COLORS['bg_primary']};
                border: none;
            }}
            QScrollBar:horizontal {{
                background-color: {COLORS['bg_secondary']};
                height: 12px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {COLORS['primary_blue']};
                border-radius: 6px;
            }}
        """)
        
        # Widget para scrollear
        scroll_widget = QWidget()
        scroll_layout = QHBoxLayout()
        scroll_layout.setSpacing(0)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        
        # Columna de entradas
        self.inputs_column = InputsColumn(self.circuit)
        self.inputs_column.setMinimumWidth(80)
        self.inputs_column.input_changed.connect(self._on_input_changed)
        scroll_layout.addWidget(self.inputs_column)
        
        # Columnas de niveles
        self.level_columns = []
        for level in range(self.circuit.levels):
            level_col = LevelColumn(
                self.circuit,
                level,
                LEVEL_COLORS[level % len(LEVEL_COLORS)]
            )
            level_col.setMinimumWidth(220)
            level_col.gate_changed.connect(self._on_gate_changed)
            scroll_layout.addWidget(level_col)
            self.level_columns.append(level_col)
        
        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        content_layout.addWidget(scroll)
        content.setLayout(content_layout)
        main_layout.addWidget(content, 1)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Aplicar estilo general
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['bg_primary']};
            }}
        """)
    
    def _on_input_changed(self, index: int, value: int):
        """Actualiza el circuito cuando cambia una entrada."""
        self._update_display()
    
    def _on_gate_changed(self, level: int, gate_type: str):
        """Actualiza el circuito cuando cambia un gate."""
        self._update_display()
    
    def _update_display(self):
        """Actualiza toda la visualización."""
        # Calcular resultados
        results = self.circuit.compute()
        
        # Actualizar columnas de niveles
        for level, level_col in enumerate(self.level_columns):
            if level < len(results):
                level_col.update_display(results[level])
        
        # Actualizar salida final
        final_output = self.circuit.get_final_output()
        self.final_output_display.setText("1" if final_output else "0")
        color = COLORS['green'] if final_output else COLORS['red']
        self.final_output_display.setStyleSheet(f"color: {color}; padding: 5px 15px; background-color: {COLORS['bg_primary']}; border-radius: 4px;")
    
    def _on_reset(self):
        """Reset de todo el circuito (entradas y tipos de compuerta)."""
        self.circuit.reset()
        # volver comboboxes a AND
        for lvl in self.level_columns:
            try:
                lvl.combo.setCurrentText("AND")
            except AttributeError:
                pass
        self.inputs_column.update_display()
        self._update_display()

    def _on_rebuild(self):
        """Solicita volver al diálogo inicial para reconstruir el circuito."""
        self.rebuild_requested.emit()
        self.close()
