from abc import ABC, abstractmethod


class Compuerta(ABC):
    """Clase abstracta que define la interfaz para todas las compuertas lógicas."""
    
    def __init__(self):
        self.flip_flop = False

    @abstractmethod
    def operar(self, A, B=None):
        """
        Realiza la operación lógica.
        
        Args:
            A: Primera entrada
            B: Segunda entrada (opcional para NOT)
        """
        pass
