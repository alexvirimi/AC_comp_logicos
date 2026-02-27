"""
Módulo de estilos - Define temas y colores para la interfaz
"""

# Colores del tema oscuro
COLORES_NEON = [
    "#f97316",  # orange
    "#f59e0b",  # amber
    "#10b981",  # emerald
    "#06b6d4",  # cyan
    "#60a5fa",  # blue
    "#a78bfa",  # purple
]

COLORES_TEMA = {
    "fondo_principal": "#0b1220",
    "fondo_secundario": "#1a2332",
    "fondo_panel": "rgba(255, 255, 255, 0.02)",
    "borde": "rgba(255, 255, 255, 0.04)",
    "texto_principal": "#e6eef8",
    "texto_secundario": "#a0aec0",
    "verde_activo": "#22c55e",
    "rojo_inactivo": "#ef4444",
    "azul_primario": "#3b82f6",
    "azul_secundario": "#60a5fa",
    "border_neon": "#dbeafe",
}

# Estilos QSS para Qt
ESTILO_APLICACION = """
QMainWindow, QWidget {
    background-color: #0b1220;
    color: #e6eef8;
}

QHeaderView::section {
    background-color: #1a2332;
    color: #e6eef8;
    padding: 5px;
    border: 1px solid rgba(255, 255, 255, 0.04);
}

QPushButton {
    background-color: #1a2332;
    color: #e6eef8;
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 5px;
    padding: 5px 10px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2a3442;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

QPushButton:pressed {
    background-color: #3a4452;
}

QComboBox {
    background-color: #1a2332;
    color: #e6eef8;
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 5px;
    padding: 5px;
}

QComboBox::drop-down {
    border: none;
}

QComboBox QAbstractItemView {
    background-color: #1a2332;
    color: #e6eef8;
    selection-background-color: #3b82f6;
}

QLabel {
    color: #e6eef8;
}

QSpinBox, QDoubleSpinBox {
    background-color: #1a2332;
    color: #e6eef8;
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 5px;
    padding: 3px;
}

QTabBar::tab {
    background-color: #1a2332;
    color: #e6eef8;
    padding: 5px 15px;
    border: 1px solid rgba(255, 255, 255, 0.04);
}

QTabBar::tab:selected {
    background-color: #3b82f6;
    border: 1px solid #3b82f6;
}

QScrollBar:vertical {
    background-color: #0b1220;
    width: 12px;
}

QScrollBar::handle:vertical {
    background-color: #3b82f6;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background-color: #60a5fa;
}

QScrollBar:horizontal {
    background-color: #0b1220;
    height: 12px;
}

QScrollBar::handle:horizontal {
    background-color: #3b82f6;
    border-radius: 6px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #60a5fa;
}
"""

# Paleta de compuertas
PALETA_COMPUERTAS = {
    "AND": {"nombre": "AND", "simbolo": "∧", "color": COLORES_NEON[0]},
    "OR": {"nombre": "OR", "simbolo": "∨", "color": COLORES_NEON[1]},
    "NAND": {"nombre": "NAND", "simbolo": "⊼", "color": COLORES_NEON[2]},
    "NOR": {"nombre": "NOR", "simbolo": "⊽", "color": COLORES_NEON[3]},
    "XOR": {"nombre": "XOR", "simbolo": "⊕", "color": COLORES_NEON[4]},
    "XNOR": {"nombre": "XNOR", "simbolo": "⊙", "color": COLORES_NEON[5]},
}
