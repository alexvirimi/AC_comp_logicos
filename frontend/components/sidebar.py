from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSlider, 
    QFrame, QHBoxLayout, QScrollArea
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QSize
from config import GATE_ASSETS

class SideBar(QWidget):
    def __init__(self, on_level_change_callback):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.on_level_change = on_level_change_callback
        self.init_ui()

    def init_ui(self):
        # Configuración estética del panel
        self.setFixedWidth(220)
        # Pueden CAMBIAR LOS COLORES Y FUENTES AQUÍ, ESO ESTA AHI DE PRUEBA
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QLabel {
                background-color: transparent;
                font-family: 'Raleway', sans-serif;
                color: #000000;
            }
        """)

        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(15, 20, 15, 20)
        layout_principal.setSpacing(10)

        # --- SECCIÓN: NÚMERO DE COMPUERTAS (Niveles) ---
        self.lbl_niveles_texto = QLabel("Número de Niveles: 1") # Texto que cambiará
        self.lbl_niveles_texto.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout_principal.addWidget(self.lbl_niveles_texto)

        self.slider_niveles = QSlider(Qt.Orientation.Horizontal)
        self.slider_niveles.setMinimum(1)
        self.slider_niveles.setMaximum(6)
        self.slider_niveles.setStyleSheet("padding: 5px;")

        self.slider_niveles.valueChanged.connect(self.actualizar_valor_slider)

        layout_principal.addWidget(self.slider_niveles)

        # --- SECCIÓN: SÍMBOLOS (Referencias) ---
        lbl_simbolos = QLabel("Símbolos")
        lbl_simbolos.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout_principal.addWidget(lbl_simbolos)

        # Subsección: Compuertas
        layout_principal.addWidget(QLabel("Compuertas"))
        self.agregar_referencia(layout_principal, "AND", GATE_ASSETS["AND"])
        self.agregar_referencia(layout_principal, "OR", GATE_ASSETS["OR"])
        self.agregar_referencia(layout_principal, "NAND", GATE_ASSETS["NAND"])
        self.agregar_referencia(layout_principal, "NOR", GATE_ASSETS["NOR"])
        self.agregar_referencia(layout_principal, "XOR", GATE_ASSETS["XOR"])
        self.agregar_referencia(layout_principal, "XNOR", GATE_ASSETS["XNOR"])

        # Subsección: Flip Flops
        layout_principal.addWidget(QLabel("Flip Flops"))
        self.agregar_referencia(layout_principal, "SR", GATE_ASSETS["FF_SR"], es_cuadrado=True)

        layout_principal.addStretch() # Esto empuja todo hacia arriba y deja espacio vacío abajo
        self.setLayout(layout_principal)
    
    def actualizar_valor_slider(self, valor):
        """Esta función actualiza la interfaz y avisa al main"""
        self.lbl_niveles_texto.setText(f"Número de Niveles: {valor}")

        if self.on_level_change:
            self.on_level_change(valor)

    def agregar_referencia(self, layout, nombre, ruta_svg, es_cuadrado=False):
        """Crea un cuadro con el icono y el nombre como en tu boceto"""
        contenedor = QFrame()
        contenedor.setStyleSheet("background: white;")
        fila = QHBoxLayout(contenedor)
        
        # Icono
        lbl_img = QLabel()
        pixmap = QPixmap(ruta_svg)
        if not pixmap.isNull():
            lbl_img.setPixmap(pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        fila.addWidget(lbl_img)
        fila.addWidget(QLabel(nombre))
        fila.addStretch()
        
        layout.addWidget(contenedor)