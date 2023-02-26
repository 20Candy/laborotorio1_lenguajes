from utils.set import Set
from graphviz import Digraph

class Automaton:
    def __init__(self):
        self.states = Set()
        self.finalStates = Set()
        self.symbols = Set()
        self.initialState = None
        self.transitions = []

    def Transicion(self, e, s):
        conjunto_destino = Set()
        for transicion in self.transitions:
            if transicion.estado_origen == e and transicion.el_simbolo == s:
                conjunto_destino = conjunto_destino.Union(transicion.estado_destino.EstadosAFN)
        return conjunto_destino


    def addState(self, estado):
        self.states.AddItem(estado)

    def addFinalState(self, estado):
        self.finalStates.AddItem(estado)

    def addSymbol(self, simbolo):
        self.symbols.AddItem(simbolo)

    def addTransition(self, origen, destino, simbolo):
        self.transitions.append((origen, destino, simbolo))

    def setSingleFinalState(self, estado):
        self.finalStates.Clear()
        self.finalStates.AddItem(estado)

    def toString(self):
        print("\n======================================= Estados =======================================")
        for estado in self.states.elements:
            print(estado)
        print("\n===================================== Transiciones =====================================")
        for transition in self.transitions:
            print(transition[0], " -> ", transition[1], " -> ", transition[2])
        print("\n==================================== Estado inicial =====================================")
        print(self.initialState)
        print("\n==================================== Estados finales ===================================")
        for estado_final in self.finalStates.elements:
            print(estado_final)
           
    def toGraph(self,automaton, name):
        g = Digraph('AFN', filename=name)
        g.attr(rankdir='LR')

        for state in automaton.states.elements:
            if state.type == 'inicial':
                g.node(str(state.id), shape='circle')
                g.node ('', shape='none', height='0', width='0')
                g.edge('', str(state.id))

            elif state.type == 'final':
                g.node(str(state.id), shape='doublecircle')
            else:
                g.node(str(state.id), shape='circle')

        for transition in automaton.transitions:
            g.edge(str(transition[0].id), str(transition[1].id), label=transition[2])

        g.view()


