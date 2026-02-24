from gates.base import Compuerta


class XOR(Compuerta):
    """Compuerta XOR: retorna 1 si las entradas son diferentes."""
    
    def operar(self, A, B=None):
        return int(A ^ B)
