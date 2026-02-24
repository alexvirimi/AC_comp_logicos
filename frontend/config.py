""" General static configuration for the frontend """
from pathlib import Path

# Buscamos la carpeta donde está este archivo
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

# Diccionario de Assets
GATE_ASSETS = {
    "INPUT": str(ASSETS_DIR / "input.svg"),
    "AND":   str(ASSETS_DIR / "and.svg"),
    "OR":    str(ASSETS_DIR / "or.svg"),
    "NAND":  str(ASSETS_DIR / "nand.svg"),
    "NOR":   str(ASSETS_DIR / "nor.svg"),
    "XOR":   str(ASSETS_DIR / "xor.svg"),
    "XNOR":  str(ASSETS_DIR / "xnor.svg"),
    "FF_SR": str(ASSETS_DIR / "flipflop_sr.svg"),
}

# Configuraciones visuales globales
COLORS = {
    "ON": "#00FF00",  # Verde para el 1
    "OFF": "#FF0000"  # Rojo para el 0
}