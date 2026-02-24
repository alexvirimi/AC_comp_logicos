"""Controlador para manejar operaciones de compuertas lógicas."""

from gates.base import Compuerta


class CompuertaController:
    """
    Controller que gestiona las operaciones de las compuertas.
    Patrón: Controller para separar lógica de negocio de la presentación.
    """
    
    def operar(self, compuerta: Compuerta, A, B=None):
        """
        Args:
            compuerta: Instancia de Compuerta a utilizar
            A: Primera entrada
            B: Segunda entrada (opcional)

        """
        return compuerta.operar(A, B)
