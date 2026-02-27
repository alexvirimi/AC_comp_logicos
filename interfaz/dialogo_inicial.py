"""Diálogo inicial para seleccionar cantidad de niveles."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from logica.compuertas import get_input_count
from recursos.constantes import COLORS, INITIAL_DIALOG_SIZE


class LevelSelectorDialog(QDialog):
    """Diálogo para seleccionar cantidad de niveles."""
    
    level_selected = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Circuito de Compuertas")
        self.setGeometry(100, 100, INITIAL_DIALOG_SIZE[0], INITIAL_DIALOG_SIZE[1])
        self.selected_levels = 3
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la UI."""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Título
        title = QLabel("Circuito de Compuertas")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['text_primary']};")
        layout.addWidget(title)
        
        # Descripción
        desc = QLabel("Selecciona el número de niveles para tu circuito")
        desc_font = QFont()
        desc_font.setPointSize(10)
        desc.setFont(desc_font)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(desc)
        
        # Slider
        slider_layout = QVBoxLayout()
        slider_layout.setSpacing(15)
        
        header = QHBoxLayout()
        label = QLabel("Niveles")
        label.setStyleSheet(f"color: {COLORS['text_primary']};")
        self.level_label = QLabel("3")
        level_font = QFont()
        level_font.setPointSize(14)
        level_font.setBold(True)
        self.level_label.setFont(level_font)
        self.level_label.setStyleSheet(f"color: {COLORS['primary_blue']};")
        header.addWidget(label)
        header.addStretch()
        header.addWidget(self.level_label)
        slider_layout.addLayout(header)
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(6)
        self.slider.setValue(3)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self._on_slider_changed)
        slider_layout.addWidget(self.slider)
        
        layout.addLayout(slider_layout)
        
        # Stats
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(10)
        
        input_label = QLabel("Entradas")
        input_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        self.input_count_label = QLabel("8")
        input_count_font = QFont()
        input_count_font.setPointSize(16)
        input_count_font.setBold(True)
        self.input_count_label.setFont(input_count_font)
        self.input_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_count_label.setStyleSheet(f"color: {COLORS['primary_blue']};")
        
        stats_layout.addWidget(input_label)
        stats_layout.addWidget(self.input_count_label)
        
        layout.addLayout(stats_layout)
        layout.addSpacing(10)
        
        # Botón
        btn = QPushButton("Construir Circuito")
        btn_font = QFont()
        btn_font.setPointSize(11)
        btn_font.setBold(True)
        btn.setFont(btn_font)
        btn.setMinimumHeight(45)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary_blue']};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2563eb;
            }}
        """)
        btn.clicked.connect(self._on_start)
        layout.addWidget(btn)
        
        self.setLayout(layout)
        self.setStyleSheet(f"QDialog {{ background-color: {COLORS['bg_primary']}; }}")
    
    def _on_slider_changed(self, value: int):
        """Actualiza labels cuando cambia el slider."""
        self.selected_levels = value
        self.level_label.setText(str(value))
        self.input_count_label.setText(str(get_input_count(value)))
    
    def _on_start(self):
        """Emite la señal y acepta el diálogo."""
        self.level_selected.emit(self.selected_levels)
        self.accept()
