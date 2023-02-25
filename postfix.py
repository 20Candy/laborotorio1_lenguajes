class Postfix:
    def __init__(self, expression, alphabet, operators, precedence):
        self.expression = expression
        self.alphabet = alphabet
        self.operators = operators
        self.precedence = precedence

        self.expression = self.FormatExpression(self.expression)

    # pasar a minusculas, quitar espacios y agregar . entre caracteres si no tiene
    def FormatExpression(self, expression):
        new_expression = expression.lower()
        new_expression = new_expression.replace(" ", "")
        new_expression = self.AddConcatenation(new_expression)
        return new_expression

    # agregar . entre caracteres si no tiene
    def AddConcatenation(self, expression):
        new_expr = ""
        for i, token in enumerate(expression):
            if i > 0:
                if token in self.alphabet and expression[i-1] in self.alphabet:
                    new_expr += "."
                elif token in self.alphabet and expression[i-1] == ')':
                    new_expr += "."
                elif token == '(' and expression[i-1] in self.alphabet:
                    new_expr += "."
                elif token == '(' and expression[i-1] == ')':
                    new_expr += "."
                elif expression[i-1] == '?' and (token in self.alphabet or token == '('):
                    new_expr += "."
                elif expression[i-1] == '*' and (token in self.alphabet or token == '('):
                    new_expr += "."
                elif expression[i-1] == '+' and (token in self.alphabet or token == '('):
                    new_expr += "."
            new_expr += token
           
        return new_expr


    # validar expresion
    def ValidateExpression(self):

        # validar que no haya caracteres invalidos
        for token in self.expression:
            if token not in self.alphabet and token not in self.operators:
                raise ValueError("Caracter invalido: " + token)

        # validar que no haya parentesis sin cerrar
        if self.expression.count('(') != self.expression.count(')'):
            raise ValueError("Parentesis sin cerrar")

        # validar que no haya un parentesis de cierre antes de un parentesis de apertura
        for i, token in enumerate(self.expression):
            if token == ')':
                if self.expression[i-1] == '(':
                    raise ValueError("Parentesis vacio")

        #validar que si es un operador binario, no este al inicio o al final
        for i, token in enumerate(self.expression):
            if token in "|." and token != '(' and token != ')':
                if i == 0 or i == len(self.expression)-1:
                    raise ValueError("Operador binario no puede estar al inicio o al final")

        #validar que si es un operador unario, debe tener un caracter o ) a la izquierda o un operador unario a la izquierda
        
        for i, token in enumerate(self.expression):
            if token in "+*?":
                if self.expression[i-1] not in self.alphabet and self.expression[i-1] != ')' and self.expression[i-1] not in "+*?":
                    raise ValueError("Operador unario debe tener un caracter o ) a la izquierda")

        #validar que si es un operador binario, debe tener un caracter o ) a la izquierda y un caracter o ( a la derecha
        for i, token in enumerate(self.expression):
            if token in ".|":
                if self.expression[i-1] not in self.alphabet and self.expression[i-1] != ')' and self.expression[i-1] not in "+*?":
                    raise ValueError("Operador binario debe tener un caracter o ) a la izquierda")
                if self.expression[i+1] not in self.alphabet and self.expression[i+1] != '(' and self.expression[i+1] not in "+*?":
                    raise ValueError("Operador binario debe tener un caracter o ( a la derecha")

        #validar que si es un operador unario no puede estar al principio
        for i, token in enumerate(self.expression):
            if token in "+*?":
                if i == 0:
                    raise ValueError("Operador unario no puede estar al principio")


    # convertir a postfix
    def ConvertToPostfix(self):

        try:
            self.ValidateExpression()

        except ValueError as e:
            print(e)
            return None

        stack = []
        postfix = ""

        for token in self.expression:
            if token in self.alphabet:
                postfix += token
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    postfix += stack.pop()
                stack.pop()
            else:
                while stack and self.precedence[token] <= self.precedence[stack[-1]]:
                    postfix += stack.pop()
                stack.append(token)

        while stack:
            postfix+=stack.pop()

        return postfix
