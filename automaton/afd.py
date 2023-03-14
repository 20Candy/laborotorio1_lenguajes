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
        statesToVisit = Set()
        states_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        state = State(states_list[counter], 'inicial', afn.epsilonClosure(afn.initialState))

        if(self.VerifyFinal(state.AFN_states)):
            afd.addFinalState(state)
            state.type = 'final_inicial'

        afd.addState(state)
        afd.initialState = state
        counter += 1

        statesToVisit.AddItem(state.AFN_states)

        while not statesToVisit.IsEmpty():
            currentState = statesToVisit.Pop()

            for symbol in afd.symbols.elements:

                states = afn.move(currentState, symbol)

                newStates = Set()
                for state in states.elements:
                    temp = afn.epsilonClosure(state)
                    newStates = newStates.Union(temp)
                    
                newStates.RemoveDuplicates()
                
                if(newStates.IsEmpty()):
                    continue
                
                if self.SetAlreadyExists(newStates, afd.states) is None:

                    if self.VerifyFinal(newStates):
                        state = State(states_list[counter], 'final', newStates)
                        afd.addFinalState(state)
                    else:
                        state = State(states_list[counter], 'normal', newStates)

                    afd.addState(state)
                    counter += 1

                    statesToVisit.AddItem(state.AFN_states)

                    if not self.VerifyTransitionExists(self.SetAlreadyExists(currentState, afd.states), state, symbol, afd):                    
                        afd.addTransition(self.SetAlreadyExists(currentState, afd.states), state, symbol)
                
                else:
                    if not self.VerifyTransitionExists(self.SetAlreadyExists(currentState, afd.states), self.SetAlreadyExists(newStates, afd.states), symbol, afd):
                        afd.addTransition(self.SetAlreadyExists(currentState, afd.states), self.SetAlreadyExists(newStates, afd.states), symbol)


        return afd
    
    def SetAlreadyExists(self, newSet, states):
        for state in states.elements:
            if len(state.AFN_states.elements) == len(newSet.elements):
                for element in state.AFN_states.elements:
                    if element not in newSet.elements:
                        break
                    else:
                        return state
        return None
    
    def VerifyFinal(self, states):
        for element in states.elements:
            if element.type == 'final':
                return True
        return False
    
    def VerifyTransitionExists(self, origin_state, destiny_state, symbol, afd):

        if afd.transitions:
            for transition in afd.transitions:
                if transition[0] == origin_state and transition[1] == destiny_state and transition[2] == symbol:
                    return True
        return False
        

    def getTransition(self, state, symbol):
        for transition in self.transitions:
            if transition[0] == state and transition[2] == symbol:
                return transition[1]
        return None
    


