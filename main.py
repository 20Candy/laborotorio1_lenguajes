from lexicalAnalyzer.scannerYapal import ScannerYapal
from lexicalAnalyzer.scannerYalex import ScannerYalex
from tree.postfix import Postfix
from tree.tree import Tree
from automaton.afn import Afn
from automaton.afd import Afd
from automaton.minimization import Minimization
from automaton.direct import Direct
from automaton.simulation import Simulation
from simulacion.simulacion import tokens
from automaton.slr import SLR


#alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ε', 'E', 'ϵ']
operators = ['|', '*', '+', '?', '(', ')', '•']
precedence = {'(': 1, "(": 1, '|': 2, '•': 3, '*': 4, '+': 4, '?': 4}
alphabet = [str(i) for i in range(256)] # ASCII

def main():

    scanner1 = ScannerYalex('./pruebas_lab_f/slr-3.yal')
    regex = scanner1.scan()


    scanner = ScannerYapal('./pruebas_lab_f/slr-3.yalp')
    tokens,productions, ignore = scanner.scan(scanner1.tokens)

    slr = SLR(tokens,productions,ignore)
    slr.SLR()
    slr.tabla()



if __name__ == "__main__":
    main()
