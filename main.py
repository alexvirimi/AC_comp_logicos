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
    
    # Mostrar diálogo inicial
    dialog = LevelSelectorDialog()

    if dialog.exec() == QDialog.DialogCode.Accepted:
        # Si el usuario selecciona niveles, mostrar ventana principal
        window = CircuitWindow(dialog.selected_levels)
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
