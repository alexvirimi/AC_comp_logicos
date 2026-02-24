from gates.base import Compuerta


class XNOR(Compuerta):
    """Compuerta XNOR: retorna 1 si las entradas son iguales."""

    def operar(self, A, B=None):
        return int(not (A ^ B))
