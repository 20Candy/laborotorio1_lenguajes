from utils.set import Set
from automaton.automaton import Automaton
from utils.state import State


class Minimization:
    def __init__(self):
        self.conjuntos = []

    def Minimize(self, afd):
        minimized = self.hopcroft(afd)

        minimized.toString()
        minimized.toGraph(minimized, "Minimized")

        return minimized
    
    def hopcroft(self, afd):

        automata = Automaton()
        automata.symbols = afd.symbols

        if (len(afd.states.Difference(afd.finalStates).elements)) != 0:
            P = [afd.finalStates, afd.states.Difference(afd.finalStates)]
            W = [afd.finalStates, afd.states.Difference(afd.finalStates)]
        else:
            P = [afd.finalStates]
            W = [afd.finalStates]

        while len(W) != 0:
            A = W[0]
            W.remove(A)

            for symbol in automata.symbols.elements:
                X = Set()

                for transition in afd.transitions:
                    if transition[2] == symbol and transition[1] in A.elements:
                        X.AddItem(transition[0])

                for Y in P:
                    if len(X.Intersection(Y)) != 0 and len(Y.Difference(X)) != 0:
                        P.remove(Y)
                        P.append(X.Intersection(Y))
                        P.append(Y.Difference(X))

                        if Y in W:
                            W.remove(Y)
                            W.append(X.Intersection(Y))
                            W.append(Y.Difference(X))
                        else:
                            if len(X.Intersection(Y).elements) <= len(Y.Difference(X).elements):
                                W.append(X.Intersection(Y))
                            else:
                                W.append(Y.Difference(X))

        self.conjuntos = P
        self.conjuntos = sorted(self.conjuntos, key=len, reverse=True)
        # self.conjuntos = sorted(self.conjuntos, key=lambda x: list(x))


        counter = 0

        for conjunto in self.conjuntos:
            state = State(counter, 'normal', conjunto)
            automata.addState(state)
            counter += 1


        for state in automata.states.elements:

            for inner_state in state.AFN_states.elements:
                if inner_state.type == 'inicial':
                    state.type = 'inicial'
                    automata.initialState = state
                    break
                if inner_state.type == 'final':
                    state.type = 'final'
                    automata.addFinalState(state)
                    break
                if inner_state.type == 'final_inicial':
                    state.type = 'final_inicial'
                    automata.addFinalState(state)
                    automata.initialState = state
                    break

           
        for transicion in afd.transitions:
            automata.addTransition(self.findState(transition[0], automata),self.findState(transicion[1], automata),transicion[2])

        return automata

    def findState(self, state, automata):
        for state1 in automata.states.elements:
            for state2 in state1.AFN_states.elements:
                if state.id == state2.id:
                    return state1
        return None