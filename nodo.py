class Nodo:
    def __init__(self, simbolo, hijo_izq=None, hijo_der=None):
        self.simbolo = simbolo
        self.hijo_izq = hijo_izq
        self.hijo_der = hijo_der

    def __str__(self):
        return self.simbolo