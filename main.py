from tree.postfix import Postfix
from tree.tree import Tree
from automaton.afn import Afn
from automaton.afd import Afd
from automaton.minimization import Minimization
from automaton.direct import Direct
from automaton.simulation import Simulation

from lexicalAnalyzer.scanner import Scanner

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ε', 'E', 'ϵ']
operators = ['|', '*', '+', '?', '(', ')', '.']
precedence = {'(': 1, "(": 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 4}

def main():

    scanner = Scanner('./yalex/slr-1.yal')
    scanner.scan()
    print(scanner)


    

    # expresion = ["(a*|b*)c", "(b|b)*abb(a|b)*", "(a|ε)b(a+)c?", "(a|b)*a(a|b)(a|b)","b*ab?", "b+abc+", "ab*ab*", "0(0|1)*0", "((ε|0)1*)*", "(0|1)*0(0|1)(0|1)", "(00)*(11)*", "(0|1)1*(0|1)", "0?(1|ε)?0*", "((1?)*)*", "(01)*(10)*"]


    # for i in range(len(expresion)):
    #     print(f"\t{i+1}. {expresion[i]}")

    # opcion = int(input("\nIngrese el número de la expresión regular a evaluar: "))

    # if opcion > 0 and opcion <= len(expresion):

    #     print("********************************************* Expresion Regular *********************************************")
    #     # expresion = input("Ingrese la expresion regular: ")
    #     postfix = Postfix(expresion[opcion-1], alphabet, operators, precedence)
        
    #     print("\n********************************************* Expresion Postfix *********************************************")
    #     postfix = postfix.ConvertToPostfix()
    #     if(postfix == None):
    #         return
    #     print(postfix)

    #     tree = Tree(postfix)
    #     tree.BuildTree()

    #     print("\n********************************************* AFN *********************************************")

    #     afn = Afn()
    #     afn = afn.BuildAfn(tree.node)

    #     print("\n********************************************* AFD *********************************************")

    #     afd = Afd()
    #     afd = afd.BuildAfd(afn)

    #     print("\n********************************************* Minimizacion *********************************************")

    #     minimization = Minimization()
    #     minimization.Minimize(afd)

    #     print("\n********************************************* Directo *********************************************")
    #     direct = Direct()
    #     direct = direct.Direct(postfix)

    #     print("\n********************************************* Minimzacion con Directo *********************************************")
    #     minimization = Minimization("MinimizationDirect")
    #     minimization.Minimize(direct)

    #     print("\n********************************************* Simulación *********************************************")
    #     cadena = input("Ingrese la cadena a evaluar: ")
    #     simulation = Simulation(afn, cadena)
    #     if(simulation.simulation()):
    #         print("La cadena es aceptada por afn")
    #     else:
    #         print("La cadena no es aceptada por afn")

    #     simulation = Simulation(afd, cadena)
    #     if(simulation.simulation()):
    #         print("La cadena es aceptada por afd subconjuntos")
    #     else:
    #         print("La cadena no es aceptada por afd subconjuntos")

    #     simulation = Simulation(direct, cadena)
    #     if(simulation.simulation()):
    #         print("La cadena es aceptada por directo")
    #     else:
    #         print("La cadena no es aceptada por directo")

        



if __name__ == "__main__":
    main()
