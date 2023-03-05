from tree.postfix import Postfix
from tree.tree import Tree
from automaton.afn import Afn
from automaton.afd import Afd
from automaton.minimization import Minimization
from automaton.direct import Direct
from automaton.simulation import Simulation

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ε', 'E', 'ϵ']
operators = ['|', '*', '+', '?', '(', ')', '.']
precedence = {'(': 1, "(": 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 4}

def main():

    print("********************************************* Expresion Regular *********************************************")
    expresion = input("Ingrese la expresion regular: ")
    postfix = Postfix(expresion, alphabet, operators, precedence)
    
    print("\n********************************************* Expresion Postfix *********************************************")
    postfix = postfix.ConvertToPostfix()
    if(postfix == None):
        return
    print(postfix)

    tree = Tree(postfix)
    tree.BuildTree()

    print("\n********************************************* AFN *********************************************")

    afn = Afn()
    afn = afn.BuildAfn(tree.node)

    print("\n********************************************* AFD *********************************************")

    afd = Afd()
    afd = afd.BuildAfd(afn)

    print("\n********************************************* Minimizacion *********************************************")

    minimization = Minimization()
    minimization.Minimize(afd)

    print("\n********************************************* Directo *********************************************")
    direct = Direct()
    direct = direct.Direct(postfix)

    print("\n********************************************* Minimzacion con Directo *********************************************")
    minimization = Minimization("MinimizationDirect")
    minimization.Minimize(direct)

    print("\n********************************************* Simulación *********************************************")
    cadena = input("Ingrese la cadena a evaluar: ")
    simulation = Simulation(afn, cadena)
    if(simulation.simulation()):
        print("La cadena es aceptada por afn")
    else:
        print("La cadena no es aceptada por afn")

    simulation = Simulation(afd, cadena)
    if(simulation.simulation()):
        print("La cadena es aceptada por afd")
    else:
        print("La cadena no es aceptada por afd")

    

if __name__ == "__main__":
    main()
