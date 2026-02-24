from gates.base import Compuerta


class OR(Compuerta):
    """Compuerta OR: retorna 1 si al menos una entrada es 1."""
    
    def operar(self, A, B=None):
        return int(A or B)
