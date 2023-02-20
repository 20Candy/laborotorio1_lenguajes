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


    def agregar_estado(self, estado):
        self.Estados.AddItem(estado)

    def agregar_estado_final(self, estado):
        self.EstadosFinales.AddItem(estado)

    def agregar_simbolo(self, simbolo):
        self.Simbolos.AddItem(simbolo)

    def agregar_transicion(self, origen, destino, simbolo):
        self.transiciones.append((origen, destino, simbolo))

    #para afn solo un estado final
    def setEstadoFinal(self, estado):
        self.EstadosFinales.clear()
        self.EstadosFinales.AddItem(estado)

    def toString(self):
        print("\n======================================= Estados =======================================")
        for estado in self.Estados.Elementos:
            print(estado)
        print("\n===================================== Transiciones =====================================")
        for transicion in self.transiciones:
            print(transicion[0], " -> ", transicion[1], " -> ", transicion[2])
        print("\n==================================== Estado inicial =====================================")
        print(self.estado_inicial)
        print("\n==================================== Estados finales ===================================")
        for estado_final in self.EstadosFinales.Elementos:
            print(estado_final)


