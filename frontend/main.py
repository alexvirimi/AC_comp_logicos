# Lo tengo mas para ir probando las cosas hay unas que sirven y otras que no, esta con Gemini y he cambiado algunas cosas 
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QGraphicsScene, QGraphicsView, QComboBox, QGraphicsProxyWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from components.input_node import InputNode
from config import GATE_ASSETS
from components.sidebar import SideBar 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador Compuertas Lógicas")
        self.resize(1200, 800)

        # 1. Widget central y Layout principal
        self.centro = QWidget()
        self.setCentralWidget(self.centro)
        self.layout_principal = QHBoxLayout(self.centro)

        # 2. Instanciar la Sidebar
        # Pasamos la función 'self.dibujar_niveles' como el callback
        self.sidebar = SideBar(on_level_change_callback=self.generar_niveles)

        # 3. Configurar la Escena (Lienzo)
        self.escena = QGraphicsScene(0, 0, 2000, 2000)
        self.vista = QGraphicsView(self.escena)

        # 4. Agregar a la interfaz
        self.layout_principal.addWidget(self.sidebar)
        self.layout_principal.addWidget(self.vista)
        self.generar_niveles(1)  # Dibuja el nivel inicial (1)

    def generar_niveles(self, nivel):
        """
        Esta función se ejecuta CADA VEZ que mueves el slider. 
        Recibe el número de niveles seleccionados y se encarga de dibujar la estructura base en el lienzo.
        """
        # Limpiamos la escena anterior
        self.escena.clear()

        ancho_columna = 250
        x_inicial = 50
        alto_base = 50

        # --- DIBUJAR LOS INPUT NODES ---
        cant_inputs = 2**nivel
        nodos_previos = []
        offset_y = 110

        for i in range(cant_inputs):
            y_pos = i * alto_base + offset_y
    
            nodo_input = InputNode(GATE_ASSETS["INPUT"])
            self.escena.addItem(nodo_input)
            nodo_input.setPos(x_inicial, y_pos)

            nodos_previos.append(y_pos)

            # --- PASO 2: DIBUJAR LAS COLUMNAS DE COMPUERTAS ---
            x_actual = x_inicial
            
            for n in range(nivel, 0, -1):
                x_actual += ancho_columna
                cant_gates = 2**(n-1)
                nodos_actuales = [] # Guardaremos las nuevas Y para la siguiente columna
                
                # Creamos el selector de este nivel
                self.crear_selector_nivel(x_actual, n, cant_gates)

                for i in range(cant_gates):
                    idx_a = i * 2
                    idx_b = i * 2 + 1
                    
                    if idx_b < len(nodos_previos):
                        y_entrada_a = nodos_previos[idx_a]
                        y_entrada_b = nodos_previos[idx_b]
                        y_gate = (y_entrada_a + y_entrada_b) / 2
                        
                        # Dibujamos la compuerta (reemplazar con GateNode después)
                        self.escena.addEllipse(x_actual, y_gate, 60, 40)
                        
                        # Dibujamos los cables para ver la conexión
                        self.escena.addLine(x_actual - ancho_columna + 30, y_entrada_a + 15, x_actual, y_gate + 10)
                        self.escena.addLine(x_actual - ancho_columna + 30, y_entrada_b + 15, x_actual, y_gate + 30)
                        
                        nodos_actuales.append(y_gate)
                    
                    nodos_previos = nodos_actuales

    def crear_selector_nivel(self, x, n, cant):
        """Genera el ComboBox que flota sobre la columna"""
        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)

        # Etiqueta de info (Nivel y cantidad)
        info = QLabel(f"NIVEL {n}\n2^{n-1} = {cant}")
        info.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        combo = QComboBox()
        combo.addItems(["AND", "OR", "NAND", "NOR", "XOR", "XNOR"])
        # Enviar el texto seleccionado
        combo.currentTextChanged.connect(lambda texto, nivel=n: self.cambiar_tipo_columna(nivel, texto))

        layout.addWidget(info)
        layout.addWidget(combo)

        proxy = QGraphicsProxyWidget()
        proxy.setWidget(contenedor)
        proxy.setPos(x - 30, 20)
        # Aseguramos que el mouse funcione en el widget
        proxy.setFocusPolicy(Qt.FocusPolicy.ClickFocus) 
        self.escena.addItem(proxy)
    
    def cambiar_tipo_columna(self, nivel, tipo_compuerta):
        """
        Esta función se activa cuando el ComboBox cambia.
        'nivel' nos dice qué columna es, 'tipo_compuerta' nos dice si es AND, OR, etc.
        """
        print(f"Columna del Nivel {nivel} ahora será de tipo: {tipo_compuerta}")
        
        # Aquí es donde buscaremos los círculos de esa columna y les 
        # cambiaremos la imagen en el siguiente paso.

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())