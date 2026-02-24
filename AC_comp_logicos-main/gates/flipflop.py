from gates.base import Compuerta


class FlipFlop(Compuerta):
    """
    FlipFlop SR (Set-Reset): Compuerta con memoria que mantiene estado.
    
    Tabla de verdad:
    S=0, R=0 -> Mantiene estado anterior
    S=1, R=0 -> Set (salida Q = 1)
    S=0, R=1 -> Reset (salida Q = 0)
    S=1, R=1 -> Aquí lo tratamos como Set (Q = 1) por especificación
    """
    
    def __init__(self):
        super().__init__()
        self.value = 0  # Estado almacenado
        self.flip_flop = True
    
    def operar(self, A, B=None):
        """
        Opera como FlipFlop SR.
        A: Set (entrada)
        B: Reset (entrada)
        
        Retorna: (Q, Q_negado)
        """
        # A es Set, B es Reset
        if A == 1 and B == 0:
            self.value = 1  # Set
        elif A == 0 and B == 1:
            self.value = 0  # Reset
        # Si A==0 y B==0, mantiene el estado anterior
        # Si A==1 y B==1, lo tratamos como Set por la corrección requerida
        if A == 1 and B == 1:
            self.value = 1
        
        return self.value, int(not self.value)
