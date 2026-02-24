from gates.base import Compuerta


class NOR(Compuerta):
    """Compuerta NOR: retorna la negación de OR."""
    
    def operar(self, A, B=None):
        return int(not (A or B))
