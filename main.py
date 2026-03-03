"""Aplicación principal de Circuito de Compuertas Lógicas.

Uso:
    python main.py
"""

import sys
from PyQt6.QtWidgets import QApplication, QDialog
from interfaz.dialogo_inicial import LevelSelectorDialog
from interfaz.ventana_principal import CircuitWindow

def main():
    """Función principal."""
    app = QApplication(sys.argv)
    
    while True:
        # Mostrar diálogo inicial
        dialog = LevelSelectorDialog()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Si el usuario selecciona niveles, mostrar ventana principal
            window = CircuitWindow(dialog.selected_levels)
            
            # Variable para rastrear si se solicitó reconstrucción
            should_rebuild = [False]
            
            def on_rebuild_requested():
                should_rebuild[0] = True
            
            # Conectar señal de reconstrucción
            window.rebuild_requested.connect(on_rebuild_requested)
            window.show()
            
            # Ejecutar la aplicación
            app.exec()
            
            # Si se solicitó reconstrucción, volver al diálogo
            # Si no, salir de la aplicación
            if not should_rebuild[0]:
                sys.exit(0)
        else:
            sys.exit(0)

if __name__ == "__main__":
    main()
