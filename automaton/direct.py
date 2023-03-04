from automaton.automaton import Automaton


class Direct():
    def __init__(self):
        self.conjuntos = []

    def Direct(self, expression_postfix):

        direct = self.directAfd(expression_postfix)
        direct.toString()
        direct.toGraph(direct, "Direct")

        return direct
    
    def directAfd(self, node):
        automata = Automaton()

