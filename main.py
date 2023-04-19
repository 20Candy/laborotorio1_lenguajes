from tree.postfix import Postfix
from tree.tree import Tree
from automaton.afn import Afn
from automaton.afd import Afd
from automaton.minimization import Minimization
from automaton.direct import Direct
from automaton.simulation import Simulation
from simulacion.simulacion import tokens

from lexicalAnalyzer.scanner import Scanner

#alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ε', 'E', 'ϵ']
operators = ['|', '*', '+', '?', '(', ')', '•']
precedence = {'(': 1, "(": 1, '|': 2, '•': 3, '*': 4, '+': 4, '?': 4}
alphabet = [str(i) for i in range(256)] # ASCII

def main():

    scanner = Scanner('./yalex/slr-3.yal')
    scanner.scan()
    postfix = Postfix(scanner.final_regex, alphabet, operators, precedence)
    postfix = postfix.ConvertToPostfix()

    print(postfix)

    tree = Tree(postfix)
    tree.BuildTree()

    direct = Direct()
    direct = direct.Direct(postfix)    

    test = "./pruebas/prueba.txt"
    with open(test, "r") as archivo:
        contenido = archivo.read()


    print("\n==================================SIMULACION==================================")   
    #crear archivo simulacion.py
    with open('./simulacion/simulacion.py', 'w') as f:
        f.write('def tokens(listaTokens):\n')
        f.write('\tfor tokenValue in listaTokens: \n')
        f.write('\t\ttoken = tokenValue[0] \n')

        for key, value in scanner.tokens.items():
            f.write('\t\tif token == ' + repr(key) + ':\n')
            if value == '':
                f.write('\t\t\treturn None\n')
            else:
                f.write('\t\t\t' + value + '\n')

        f.write('\t\telse: \n\t\t\treturn ' + '"Error sintactico"')

    #crear simulacion
    simulation = Simulation(direct, contenido)

    #mandar simulacion a simulacion.py
    tokens(simulation.result)


    


if __name__ == "__main__":
    main()
