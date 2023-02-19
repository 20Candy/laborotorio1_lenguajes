from nodo import Nodo

import pydot


class Arbol:
    def __init__(self, expresion):
        self.expresion = expresion
        self.nodo = None
        self.pila = []
        self.contador = 1

    
    def construir_arbol(self):
        for simbolo in self.expresion:
            if simbolo == '*':
                self.crear_nodo(simbolo)
            elif simbolo == '+':
                self.crear_nodo(simbolo)
            elif simbolo == '?':
                self.crear_nodo(simbolo)
            elif simbolo == '.':
                self.crear_nodo(simbolo)
            elif simbolo == '|':
                self.crear_nodo(simbolo)
            else:
                self.crear_nodo(simbolo)

        self.nodo = self.pila.pop()
        self.graficar_arbol(self.nodo)


    def crear_nodo(self, simbolo):

        if simbolo == '*':
            nodo = Nodo(simbolo)
            nodo.hijo_izq = self.pila.pop()
            self.pila.append(nodo)
        elif simbolo == '+':
            nodo = Nodo(simbolo)
            nodo.hijo_izq = self.pila.pop()
            self.pila.append(nodo)
        elif simbolo == '?':
            nodo = Nodo(simbolo)
            nodo.hijo_izq = self.pila.pop()
            self.pila.append(nodo)
        elif simbolo == '.':
            nodo = Nodo(simbolo)
            nodo.hijo_der = self.pila.pop()
            nodo.hijo_izq = self.pila.pop()
            self.pila.append(nodo)
        elif simbolo == '|':
            nodo = Nodo(simbolo)
            nodo.hijo_der = self.pila.pop()
            nodo.hijo_izq = self.pila.pop()
            self.pila.append(nodo)
        else:
            nodo = Nodo(simbolo)
            self.pila.append(nodo)


    def graficar_arbol(self, nodo):
        graph = pydot.Dot(graph_type='graph')
        self.graficar_nodo(nodo, graph)
        graph.write_png('arbol.png')

    
    def graficar_nodo(self, nodo, graph):
        if nodo is None:
            return

        # Crear el nodo raíz con un identificador fijo y el símbolo del nodo raíz
        if nodo == self.nodo:
            nodo_actual = pydot.Node("raiz", label=nodo.simbolo)
            graph.add_node(nodo_actual)
        else:
            # Crear el nodo con un identificador incremental y el símbolo del nodo
            nodo_actual = pydot.Node(str(self.contador), label=nodo.simbolo)
            graph.add_node(nodo_actual)

        if nodo.hijo_izq is not None:
            self.contador += 1
            nodo_izq = pydot.Node(str(self.contador), label=nodo.hijo_izq.simbolo)
            graph.add_node(nodo_izq)
            self.graficar_nodo(nodo.hijo_izq, graph)
            graph.add_edge(pydot.Edge(nodo_actual, nodo_izq))

        if nodo.hijo_der is not None:
            self.contador += 1
            nodo_der = pydot.Node(str(self.contador), label=nodo.hijo_der.simbolo)
            graph.add_node(nodo_der)
            self.graficar_nodo(nodo.hijo_der, graph)
            graph.add_edge(pydot.Edge(nodo_actual, nodo_der))


    
