from postfix import Postfix
from arbol import Arbol
from afn import AFN


#alfabeto, operadores y precedencia
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ε']
operators = ['|', '*', '+', '?', '(', ')', '.']
precedence = {'(': 1, "(": 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 4}

def main():
    postfix_ = Postfix("(a*)*", alphabet, operators, precedence)
    # postfix_ = Postfix("ab*ab*", alphabet, operators, precedence)
    # postfix_ = Postfix("ab*ab*", alphabet, operators, precedence)
    # postfix_ = Postfix("0?(1?)?0*", alphabet, operators, precedence)
    # postfix_ = Postfix("(a*|b*)c", alphabet, operators, precedence)
    # postfix_ = Postfix("(b|b)*abb(a|b)*", alphabet, operators, precedence)
    # postfix_ = Postfix("(a|ε)b(a+)c?", alphabet, operators, precedence)
    # postfix_ = Postfix("(a|b)*a(a|b)(a|b)", alphabet, operators, precedence)

    
    print("\n======================================= Expresion Postfix =======================================")
    postfix = postfix_.ConvertToPostfix()
    if(postfix == None):
        return
    print(postfix)

    print("\n======================================= Arbol de Expresion =======================================")
    

    arbol = Arbol(postfix)
    arbol.construir_arbol()

    print("\n============================================ Automata ============================================")
    afn = AFN()
    afn.construir_afn(arbol.nodo)

if __name__ == "__main__":
    main()