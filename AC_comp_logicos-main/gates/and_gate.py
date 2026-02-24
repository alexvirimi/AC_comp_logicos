from gates.base import Compuerta


class AND(Compuerta):
    """Compuerta AND: retorna 1 si ambas entradas son 1."""
    
    def operar(self, A, B=None):
        return int(A and B)
