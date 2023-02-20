from postfix import Postfix
from arbol import Arbol
from afn import AFN


#alfabeto, operadores y precedencia
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ε']
operators = ['|', '*', '+', '?', '(', ')', '.']
precedence = {'(': 1, "(": 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 4}

def main():
    #expresion regular
    # expression = input("Ingrese la expresion regular: ")

    #convertir a postfix
    # postfix_ = Postfix(expression, alphabet, operators, precedence)
    # postfix = postfix_.ConvertToPostfix()
    # print(postfix)

    postfix_ = Postfix("(a|ε)b(a+)c?", alphabet, operators, precedence)
    postfix = postfix_.ConvertToPostfix()
    print("Expresion Postfix:" + postfix)

    arbol = Arbol(postfix)
    arbol.construir_arbol()

    afn = AFN()
    thompson = afn.Thompson(arbol.nodo)
    thompson.graficar("thompson")

    # postfix_ = Postfix("0?(1?)?0*", alphabet, operators, precedence)
    # postfix = postfix_.ConvertToPostfix()
    # print(postfix)
    # postfix_ = Postfix("(a*|b*)c", alphabet, operators, precedence)
    # postfix = postfix_.ConvertToPostfix()
    # print(postfix)
    # postfix_ = Postfix("(b|b)*abb(a|b)*", alphabet, operators, precedence)
    # postfix = postfix_.ConvertToPostfix()
    # print(postfix)
    # postfix_ = Postfix("(a|ε)b(a+)c?", alphabet, operators, precedence)
    # postfix = postfix_.ConvertToPostfix()
    # print(postfix)
    # postfix_ = Postfix("(a|b)*a(a|b)(a|b)", alphabet, operators, precedence)
    # postfix = postfix_.ConvertToPostfix()
    # print(postfix)



if __name__ == "__main__":
    main()