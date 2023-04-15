from utils.set import Set

class Simulation:
    def __init__(self, automaton, input):
        self.automaton = automaton
        self.input = input
        self.cadena = ""
    
    def simulation(self):
        afn = False
        for transition in self.automaton.transitions:
            if transition[2] == 'ε':
                afn = True
                break
            
        current_states = Set()
        current_states.AddItem(self.automaton.initialState)
        if afn:
            for state in self.automaton.epsilonClosure(self.automaton.initialState).elements:
                if self.stateAlreadyExists(state, current_states) is None:
                    current_states.AddItem(state)

        for symbol in self.input:
            next_states = Set()
            for state in current_states.elements:
                for transition in self.automaton.transitions:
                    if transition[0].id == state.id and chr(int(transition[2])) == symbol:
                        if self.stateAlreadyExists(transition[1], next_states) is None:
                            next_states.AddItem(transition[1])

            if next_states.IsEmpty():
                print("Error lexico")
                return False
            
            if afn:
                for state in next_states.elements:
                    for epsilon_state in self.automaton.epsilonClosure(state).elements:
                        if self.stateAlreadyExists(epsilon_state, next_states) is None:
                            next_states.AddItem(epsilon_state)
                        
            if next_states.IsEmpty():
                return False
            
            current_states = next_states

            self.cadena += symbol



        for state in current_states.elements:
            if state in self.automaton.finalStates.elements:
                print(self.cadena, state.token)
                return True
        
        print("Error lexico")
        return False
    
    def stateAlreadyExists(self, state, states):
        for element in states.elements:
            if element.id == state.id:
                return element
        return None       

