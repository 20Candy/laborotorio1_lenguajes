from set import Set

class Automata:
    def __init__(self):
        self.Estados = Set()
        self.EstadosFinales = Set()
        self.Simbolos = Set()
        self.estado_inicial = None
        self.transiciones = []

    def Transicion(self, e, s):
        conjunto_destino = Set()
        for transicion in self.transiciones:
            if transicion.estado_origen == e and transicion.el_simbolo == s:
                conjunto_destino = conjunto_destino.Union(transicion.estado_destino.EstadosAFN)
        return conjunto_destino
