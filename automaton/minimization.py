from utils.set import Set
from automaton.automaton import Automaton
from utils.state import State


class Minimization:
    def __init__(self):
        self.partition = Set()


    def Minimize(self, afd):
        minimized = self.hopcroft(afd)

        minimized.toString()
        minimized.toGraph(minimized, "Minimized")

        return minimized
    
    def hopcroft(self, afd):
        minimized = Automaton()
        minimized.symbols = afd.symbols
        minimized.initialState = afd.initialState
        minimized.finalStates = afd.finalStates
        minimized.states = afd.states

        self.partition.AddItem(afd.finalStates)
        self.partition.AddItem(afd.states.Difference(afd.finalStates))

        while True:
            new_partition = self.split(self.partition, minimized)
            if new_partition.Difference(self.partition).IsEmpty():
                break
            self.partition = new_partition

        for partition in self.partition.elements:
            state = State(partition.elements[0].id, 'normal')
            minimized.addState(state)
            if partition.Contains(afd.initialState):
                minimized.initialState = state
            if partition.Contains(afd.finalStates):
                minimized.addFinalState(state)

        for partition in self.partition.elements:
            for symbol in minimized.symbols.elements:
                states = Set()
                for state in partition.elements:
                    states = states.Union(afd.move(state, symbol))
                for new_partition in self.partition.elements:
                    if states.Equals(new_partition):
                        for state in partition.elements:
                            minimized.addTransition(state, new_partition.elements[0], symbol)
                        break

        return minimized
    
    def split(self, partition, afd):
        new_partition = Set()
        for state in partition.elements:
            for symbol in afd.symbols.elements:
                states = Set()
                for state2 in partition.elements:
                    states = states.Union(afd.move(state2, symbol))
                for new_partition in self.partition.elements:
                    if states.Difference(new_partition).IsEmpty():
                        if new_partition not in new_partition.elements:
                            new_partition.AddItem(new_partition)
                        break
        return new_partition

        

