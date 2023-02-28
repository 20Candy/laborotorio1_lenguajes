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
            new_partition = Set()
            for partition in self.partition.elements:
                partition = self.split(partition, minimized)
                new_partition = new_partition.Union(partition)
            if new_partition.Equals(self.partition):
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
                states = afd.move(state, symbol)
                for new_partition in self.partition.elements:
                    if states.Equals(new_partition):
                        new_partition.AddItem(state)
                        break
        return new_partition


        

