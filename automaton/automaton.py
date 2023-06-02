from utils.set import Set
from graphviz import Digraph

class Automaton:
    def __init__(self):
        self.states = Set()
        self.finalStates = Set()
        self.symbols = Set()
        self.initialState = None
        self.transitions = []
        self.tokens = []

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
                g.node(str(state.id), shape='square', style='filled', fillcolor='green')
                g.node ('', shape='none', height='0', width='0')
                g.edge('', str(state.id))

            elif state.type == 'final_inicial':
                g.node(str(state.id), shape='square', style='filled', fillcolor='red')
                g.node ('', shape='none', height='0', width='0')
                g.edge('', str(state.id))

            elif state.type == 'final':
                g.node(str(state.id), shape='square', style='filled', fillcolor='red')
            else:
                g.node(str(state.id), shape='square')
                

        for transition in automaton.transitions:
            g.edge(str(transition[0].id), str(transition[1].id), label=transition[2])

        g.view()

    
    def epsilonClosure(self, estado):
        visited = Set()
        stack = [estado]
        result = Set()

        while stack:
            estado = stack.pop(0)
            if estado in visited.elements:
                continue
            visited.AddItem(estado)
            result.AddItem(estado)

            for transicion in self.transitions:
                if transicion[0].id == estado.id:
                    if (transicion[2] == 'ε' and transicion[1].id != estado.id and transicion[1] not in visited.elements):
                        stack.append(transicion[1])

        return result
    
    def move(self, states, symbol):

        move = Set()
        for state in states.elements:
            for transition in self.transitions:
                if transition[0].id == state.id and transition[2] == symbol:
                    move.AddItem(transition[1])
        return move
