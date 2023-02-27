from utils.set import Set
from graphviz import Digraph

class Automaton:
    def __init__(self):
        self.states = Set()
        self.finalStates = Set()
        self.symbols = Set()
        self.initialState = None
        self.transitions = []

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

            elif state.type == 'final_inicial':
                g.node(str(state.id), shape='doublecircle')
                g.node ('', shape='none', height='0', width='0')
                g.edge('', str(state.id))

            elif state.type == 'final':
                g.node(str(state.id), shape='doublecircle')
            else:
                g.node(str(state.id), shape='circle')
                

        for transition in automaton.transitions:
            g.edge(str(transition[0].id), str(transition[1].id), label=transition[2])

        g.view()

    
    def epsilonClosure(self, state):

        closure = Set()
        closure.AddItem(state)
        for transition in self.transitions:
            if transition[0].id == state.id and transition[2] == 'ε':
                closure = closure.Union(self.epsilonClosure(transition[1]))
        return closure
    
    def move(self, states, symbol):

        move = Set()
        for state in states.elements:
            for transition in self.transitions:
                if transition[0].id == state.id and transition[2] == symbol:
                    move.AddItem(transition[1])
        return move
