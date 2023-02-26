from automaton.automaton import Automaton
from utils.state import State
from utils.set import Set

class Afn(Automaton):
    def __init__(self):
        super().__init__()
        self.counter = 0

    def BuildAfn(self, nodo):
        afn = self.Thompson(nodo)

        #eliminar simbolos repetidos
        for symbol in afn.symbols.elements:
            if afn.symbols.elements.count(symbol) > 1:
                afn.symbols.RemoveItem(symbol)

        if afn is not None:
            for state in afn.states.elements:
                for state2 in afn.states.elements:
                    if state.id == state2.id and state is not state2:
                        afn.states.elements.remove(state2)

            afn.states.elements.sort(key=lambda x: x.id)
            afn.states.elements[0].type = 'inicial'
            afn.setSingleFinalState(afn.states.elements[-1])
            afn.states.elements[-1].type = 'final'

        afn.toString()
        afn.toGraph(afn,"AFN")

        return afn
            
    def Thompson(self, nodo):

        if nodo.left_child is None and nodo.right_child is None:

            afn = Afn()

            afn.initialState = State(self.counter, 'normal')
            afn.addState(afn.initialState)

            finalStates = State(self.counter + 1, 'normal')
            afn.setSingleFinalState(finalStates)
            afn.addState(finalStates)
            
            self.counter += 1

            afn.addTransition(afn.initialState, finalStates, nodo.symbol)
            afn.addSymbol(nodo.symbol)

            return afn
            
        if nodo.symbol == '|':

            afn = Afn()

            afn.initialState = State(self.counter, 'normal')
            afn.addState(afn.initialState)
            self.counter += 1

            afn_left = self.Thompson(nodo.left_child)
            afn.addTransition(afn.initialState, afn_left.initialState, 'ε')
            self.counter += 1

            afn_right = self.Thompson(nodo.right_child)
            afn.addTransition(afn.initialState, afn_right.initialState, 'ε')

            finalStates = State(self.counter + 1, 'normal')
            afn.setSingleFinalState(finalStates)
            afn.addState(finalStates)
            self.counter += 1

            afn.addTransition(afn_left.finalStates.elements[-1], finalStates, 'ε')
            afn.addTransition(afn_right.finalStates.elements[-1], finalStates, 'ε')

            afn.addSymbol('ε')

            afn.states = afn.states.Union(afn_left.states)
            afn.states = afn.states.Union(afn_right.states)

            afn.symbols = afn.symbols.Union(afn_left.symbols)
            afn.symbols = afn.symbols.Union(afn_right.symbols)

            afn.transitions = afn.transitions + afn_left.transitions + afn_right.transitions
                        
            return afn

        if nodo.symbol == '.':       
            afn = Afn()

            afn.initialState = State(self.counter, 'normal')
            afn.addState(afn.initialState)
            
            afn_left = self.Thompson(nodo.left_child)

            afn_right = self.Thompson(nodo.right_child)

            afn.setSingleFinalState(afn_right.finalStates.elements[-1])

            afn.states = afn.states.Union(afn_left.states)
            afn.states = afn.states.Union(afn_right.states)

            afn.symbols = afn.symbols.Union(afn_left.symbols)
            afn.symbols = afn.symbols.Union(afn_right.symbols)

            afn.transitions = afn.transitions + afn_left.transitions + afn_right.transitions
            
            return afn
        
        if nodo.symbol == '?':

            afn = Afn()

            afn.initialState = State(self.counter, 'normal')
            afn.addState(afn.initialState)
            self.counter += 1

            afn_left = self.Thompson(nodo.left_child)
            afn.addTransition(afn.initialState, afn_left.initialState, 'ε')

            intermediate_state1 = State(self.counter +1, 'normal')
            afn.addState(intermediate_state1)
            self.counter += 1

            afn.addTransition(afn.initialState, intermediate_state1, 'ε')

            intermediateState2 = State(self.counter +1, 'normal')
            afn.addState(intermediateState2)
            self.counter += 1

            afn.addTransition(intermediate_state1, intermediateState2, 'ε')
            
            finalStates = State(self.counter + 1, 'normal')
            afn.setSingleFinalState(finalStates)
            afn.addState(finalStates)
            self.counter += 1

            afn.addTransition(afn_left.finalStates.elements[-1], finalStates, 'ε')
            afn.addTransition(intermediateState2, finalStates, 'ε')

            afn_left.setSingleFinalState(finalStates)

            afn.addSymbol('ε')

            afn.states = afn.states.Union(afn_left.states)
            afn.symbols = afn.symbols.Union(afn_left.symbols)
            afn.transitions = afn.transitions + afn_left.transitions
            afn.setSingleFinalState(afn_left.finalStates.elements[-1])
                        
            return afn

        if nodo.symbol == '*':

            afn = Afn()

            afn.initialState = State(self.counter, 'normal')
            afn.addState(afn.initialState)
            self.counter += 1

            afn_left = self.Thompson(nodo.left_child)
            afn.addTransition(afn.initialState, afn_left.initialState, 'ε')

            finalStates = State(self.counter + 1, 'normal')
            afn.setSingleFinalState(finalStates)
            afn.addState(finalStates)
            self.counter += 1

            afn.addTransition(afn_left.finalStates.elements[-1], finalStates, 'ε')
            afn.addTransition(afn_left.finalStates.elements[-1], afn_left.initialState, 'ε')
            afn.addTransition(afn.initialState, finalStates, 'ε')

            afn.addSymbol('ε')

            afn.states = afn.states.Union(afn_left.states)
            afn.symbols = afn.symbols.Union(afn_left.symbols)
            afn.transitions = afn.transitions + afn_left.transitions
           
            return afn

        if nodo.symbol == '+':

            afn = Afn()

            afn.initialState = State(self.counter, 'normal')
            afn.addState(afn.initialState)

            intermediateState = State(self.counter +1, 'normal')
            afn.addState(intermediateState)
            self.counter += 2

            afn.addTransition(afn.initialState, intermediateState, nodo.left_child.simbolo)

            afn.addSymbol(nodo.left_child.simbolo)

            afn_left = self.Thompson(nodo.left_child)
            afn.addTransition(intermediateState, afn_left.initialState , 'ε')

            finalStates = State(self.counter + 1, 'normal')
            afn.setSingleFinalState(finalStates)
            afn.addState(finalStates)
            self.counter += 1

            afn.addTransition(afn_left.finalStates.elements[-1], finalStates, 'ε')
            afn.addTransition(afn_left.finalStates.elements[-1], afn_left.initialState, 'ε')
            afn.addTransition(intermediateState, finalStates, 'ε')

            afn.addSymbol('ε')
            afn.states = afn.states.Union(afn_left.states)
            afn.symbols = afn.symbols.Union(afn_left.symbols)
            afn.transitions = afn.transitions + afn_left.transitions

            return afn
         
    def epsilonClosure(self, state):

        closure = Set()
        closure.AddItem(state)
        for transition in self.transitions:
            if transition[0] == state and transition[2] == 'ε':
                closure = closure.Union(self.epsilonClosure(transition[1]))
        return closure
    
    def move(self, states, symbol):

        move = Set()
        for state in states.elements:
            for transition in self.transitions:
                if transition[0] == state and transition[2] == symbol:
                    move.AddItem(transition[1])
        return move
