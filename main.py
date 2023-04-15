from tree.postfix import Postfix
from tree.tree import Tree
from automaton.afn import Afn
from automaton.afd import Afd
from automaton.minimization import Minimization
from automaton.direct import Direct
from automaton.simulation import Simulation

from lexicalAnalyzer.scanner import Scanner

#alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ε', 'E', 'ϵ']
operators = ['|', '*', '+', '?', '(', ')', '•']
precedence = {'(': 1, "(": 1, '|': 2, '•': 3, '*': 4, '+': 4, '?': 4}
alphabet = [str(i) for i in range(256)] # ASCII

def main():

    scanner = Scanner('./yalex/slr-2.yal')
    scanner.scan()
    postfix = Postfix(scanner.final_regex, alphabet, operators, precedence)
    postfix = postfix.ConvertToPostfix()

    print(postfix)

    tree = Tree(postfix)
    tree.BuildTree()

    direct = Direct()
    direct = direct.Direct(postfix)    

    test = "./pruebas/prueba.txt"
    with open(test) as f:
        testLines = f.readlines()
        
    # simulation = Simulation(testLines, direct)
    # simulation.simulate()



if __name__ == "__main__":
    main()
