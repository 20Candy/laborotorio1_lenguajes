from automaton.automaton import Automaton
from utils.set import Set
from utils.state import State

class Afd(Automaton):
    def __init__(self):
        super().__init__()

    def BuildAfd(self, afn):
        afd = self.Subconjuntos(afn)

        afd.toString()
        afd.toGraph(afd,"AFD")

        return afd

    def Subconjuntos(self, afn):

        afd = Afd()
        afd.symbols = afn.symbols
        if 'ε' in afd.symbols.elements:
            afd.symbols.RemoveItem('ε')

        counter = 0
        final = False
        statesToVisit = Set()
        states_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        state = State(states_list[counter], 'inicial', afn.epsilonClosure(afn.initialState))
        afd.addState(state)
        afd.initialState = state
        counter += 1

        statesToVisit.AddItem(state.AFN_states)

        while not statesToVisit.IsEmpty():
            currentState = statesToVisit.Pop()

            for symbol in afd.symbols.elements:

                states = afn.move(currentState, symbol)

                for state in states.elements:
                    newStates = afn.epsilonClosure(state)
                
                if self.SetAlreadyExists(newStates, afd.states) is None:

                    for newState in newStates.elements:
                        if newState.type == 'final':
                            final = True
                        
                    if final:
                        state = State(states_list[counter], 'final', newStates)
                        final = False
                    else:
                        state = State(states_list[counter], 'normal', newStates)

                    afd.addState(state)
                    counter += 1

                    statesToVisit.AddItem(state.AFN_states)
                    
                    afd.addTransition(self.SetAlreadyExists(currentState, afd.states), state, symbol)


        return afd
    
    def SetAlreadyExists(self, newSet, states):
        for state in states.elements:
            if state.AFN_states == newSet:
                return state
            
        return None
        
    


