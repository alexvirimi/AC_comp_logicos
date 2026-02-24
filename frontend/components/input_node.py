"""
Clase para las entradas:
Al presionar el botón de entrada, el valor de la entrada se alterna entre 0 y 1. 
El círculo cambia de color para reflejar el estado actual (rojo para 0 y verde para 1). 
El texto dentro del círculo muestra el valor actual de la entrada (0 o 1).
"""
import os
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from config import COLORS

class InputNode(QGraphicsSvgItem):
    def __init__(self, asset_path):
        super().__init__()
        
        # 1. Guardamos la ruta del archivo y el estado inicial (apagado = 0)
        self.asset_path = asset_path
        self.state = 0 
        
        # 2. Leemos el archivo XML original una sola vez para tenerlo como "plantilla"
        if os.path.exists(self.asset_path):
            with open(self.asset_path, 'r') as f:
                self.svg_template = f.read()
        else:
            print(f"Error: No se encontró el archivo en {self.asset_path}")
            self.svg_template = ""

        # 3. Dibujamos el estado inicial
        self.update_visuals()

        # 4. Hacemos que el objeto se pueda mover con el ratón en la pantalla
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable)

    def update_visuals(self):
        """Esta función cambia el color y el texto del dibujo SVG"""
        # Definimos el color según el estado
        color = COLORS["ON"] if self.state == 1 else COLORS["OFF"]
        texto = str(self.state)

        # Modificamos el texto del XML dinámicamente
        nuevo_xml = self.svg_template.replace('fill="red"', f'fill="{color}"')
        nuevo_xml = nuevo_xml.replace('>0<', f'>{texto}<')

        # El motor de PyQt6 (QSvgRenderer) toma el texto modificado y lo convierte en imagen
        self.renderer = QSvgRenderer(nuevo_xml.encode('utf-8'))
        self.setSharedRenderer(self.renderer)
        self.update() # Refresca la pantalla

    def mousePressEvent(self, event):
        """Alterna el estado entre 0 y 1 cada vez que se hace clic en la entrada"""
        # Cambiamos el estado: si era 0 pasa a 1, si era 1 pasa a 0
        self.state = 1 if self.state == 0 else 0
        
        # Llamamos a la función para que el dibujo cambie de color
        self.update_visuals()

        # Esto le dice a PyQt6 que el evento se procesó correctamente
        super().mousePressEvent(event)