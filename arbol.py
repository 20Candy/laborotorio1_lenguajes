from nodo import Nodo

from graphviz import Digraph

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
        dot = Digraph(comment='Árbol sintáctico')
        self.graficar_nodo(nodo, dot)
        dot.render('arbol', view=True)

    def graficar_nodo(self, nodo, dot):
        if nodo is None:
            return

        # Crear el nodo con el símbolo del nodo
        dot.node(str(id(nodo)), label=nodo.simbolo)

        if nodo.hijo_izq is not None:
            self.graficar_nodo(nodo.hijo_izq, dot)
            dot.edge(str(id(nodo)), str(id(nodo.hijo_izq)))

        if nodo.hijo_der is not None:
            self.graficar_nodo(nodo.hijo_der, dot)
            dot.edge(str(id(nodo)), str(id(nodo.hijo_der)))

    
