from automata import Automata
from estado import Estado
from transicion import Transicion

from graphviz import Digraph

class AFN(Automata):
    def __init__(self):
        super().__init__()
        self.contador = 0


    def construir_desde_arbol(self, arbol):
        self.contador = 0
        self.estado_inicial = self.construir_desde_arbol_recursivo(arbol)
        self.Estados.AddItem(self.estado_inicial)
        self.EstadosFinales.AddItem(self.estado_inicial)
        
    def construir_desde_arbol_recursivo(self, arbol):
        if arbol.hijo_izq is None and arbol.hijo_der is None:
            estado = Estado(self.contador, 'normal')
            self.contador += 1
            return estado
        elif arbol.hijo_izq is not None and arbol.hijo_der is None:
            estado = Estado(self.contador, 'normal')
            self.contador += 1
            estado_hijo_izq = self.construir_desde_arbol_recursivo(arbol.hijo_izq)
            self.Estados.AddItem(estado_hijo_izq)
            self.transiciones.append(Transicion(estado, estado_hijo_izq, arbol.simbolo))
            return estado
        elif arbol.hijo_izq is None and arbol.hijo_der is not None:
            estado = Estado(self.contador, 'normal')
            self.contador += 1
            estado_hijo_der = self.construir_desde_arbol_recursivo(arbol.hijo_der)
            self.Estados.AddItem(estado_hijo_der)
            self.transiciones.append(Transicion(estado, estado_hijo_der, arbol.simbolo))
            return estado
        elif arbol.hijo_izq is not None and arbol.hijo_der is not None:
            if arbol.simbolo == '*':
                estado = Estado(self.contador, 'normal')
                self.contador += 1
                estado_hijo_izq = self.construir_desde_arbol_recursivo(arbol.hijo_izq)
                self.Estados.AddItem(estado_hijo_izq)
                self.transiciones.append(Transicion(estado, estado_hijo_izq, arbol.simbolo))
                self.transiciones.append(Transicion(estado_hijo_izq, estado, arbol.simbolo))
                return estado
            elif arbol.simbolo == '|':
                estado = Estado(self.contador, 'normal')
                self.contador += 1
                estado_hijo_izq = self.construir_desde_arbol_recursivo(arbol.hijo_izq)
                self.Estados.AddItem(estado_hijo_izq)
                estado_hijo_der = self.construir_desde_arbol_recursivo(arbol.hijo_der)
                self.Estados.AddItem(estado_hijo_der)
                self.transiciones.append(Transicion(estado, estado_hijo_izq, arbol.simbolo))
                self.transiciones.append(Transicion(estado, estado_hijo_der, arbol.simbolo))
                return estado
            elif arbol.simbolo == '.':
                estado = Estado(self.contador, 'normal')
                self.contador += 1
                estado_hijo_izq = self.construir_desde_arbol_recursivo(arbol.hijo_izq)
                self.Estados.AddItem(estado_hijo_izq)
                estado_hijo_der = self.construir_desde_arbol_recursivo(arbol.hijo_der)
                self.Estados.AddItem(estado_hijo_der)
                self.transiciones.append(Transicion(estado, estado_hijo_izq, arbol.simbolo))
                self.transiciones.append(Transicion(estado_hijo_izq, estado_hijo_der, arbol.simbolo))
                return estado_hijo_der
            elif arbol.simbolo == '+':
                estado = Estado(self.contador, 'normal')
                self.contador += 1
                estado_hijo_izq = self.construir_desde_arbol_recursivo(arbol.hijo_izq)
                self.Estados.AddItem(estado_hijo_izq)
                estado_hijo_der = self.construir_desde_arbol_recursivo(arbol.hijo_der)
                self.Estados.AddItem(estado_hijo_der)
                self.transiciones.append(Transicion(estado, estado_hijo_izq, arbol.simbolo))
                self.transiciones.append(Transicion(estado_hijo_izq, estado_hijo_der, arbol.simbolo))
                self.transiciones.append(Transicion(estado_hijo_der, estado_hijo_izq, arbol.simbolo))
                return estado

    def cerradura_epsilon(self, conjunto_estados):
        conjunto_resultado = conjunto_estados
        for estado in conjunto_estados.Elementos:
            for transicion in self.transiciones:
                if transicion.estado_origen == estado and transicion.el_simbolo == '*':
                    conjunto_resultado = conjunto_resultado.Union(transicion.estado_destino.EstadosAFN)
        return conjunto_resultado

    def mover(self, conjunto_estados, simbolo):
        conjunto_resultado = Estado()
        for estado in conjunto_estados.Elementos:
            for transicion in self.transiciones:
                if transicion.estado_origen == estado and transicion.el_simbolo == simbolo:
                    conjunto_resultado = conjunto_resultado.Union(transicion.estado_destino.EstadosAFN)
        return conjunto_resultado

    def evaluar_cadena(self, cadena):
        conjunto_estados = self.cerradura_epsilon(self.estado_inicial.EstadosAFN)
        for simbolo in cadena:
            conjunto_estados = self.mover(conjunto_estados, simbolo)
            conjunto_estados = self.cerradura_epsilon(conjunto_estados)
        for estado in conjunto_estados.Elementos:
            if estado in self.EstadosFinales.Elementos:
                return True
        return False    



    def graficar(self, nombre_archivo):
        from graphviz import Digraph

        g = Digraph('AFN', filename=nombre_archivo)

        # Agregar los estados al grafo
        for estado in self.Estados.Elementos:
            if estado in self.EstadosFinales.Elementos:
                g.node(str(estado.id), label=str(estado.id), shape='doublecircle')
            else:
                g.node(str(estado.id), label=str(estado.id), shape='circle')

        # Agregar las transiciones al grafo
        for transicion in self.transiciones:
            g.edge(str(transicion.estado_origen.id), str(transicion.estado_destino.id), label=transicion.el_simbolo)

        g.view()


