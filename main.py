from postfix import Postfix
from arbol import Arbol
from afn import AFN


#alfabeto, operadores y precedencia
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ε']
operators = ['|', '*', '+', '?', '(', ')', '.']
precedence = {'(': 1, "(": 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 4}

def main():

    print("======================================= Expresion Regular =======================================")
    expresion = input("Ingrese la expresion regular: ")
    postfix_ = Postfix(expresion, alphabet, operators, precedence)
    
    print("\n======================================= Expresion Postfix =======================================")
    postfix = postfix_.ConvertToPostfix()
    if(postfix == None):
        return
    print(postfix)

    # print("\n======================================= Arbol de Expresion =======================================")

    arbol = Arbol(postfix)
    arbol.construir_arbol()

    # print("\n============================================ Automata ============================================")
    afn = AFN()
    afn.construir_afn(arbol.nodo)

if __name__ == "__main__":
    main()