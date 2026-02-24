from gates.base import Compuerta


class NAND(Compuerta):
    """Compuerta NAND: retorna la negación de AND."""
    
    def operar(self, A, B=None):
        return int(not (A and B))
