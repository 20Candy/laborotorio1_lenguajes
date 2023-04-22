class Postfix:
    def __init__(self, scanner, alphabet, operators, precedence):
        self.expression = scanner.final_regex
        self.tokens = scanner.tokens.keys()
        self.alphabet = self.TokenAlphabet(alphabet,self.tokens)
        self.operators = operators
        self.precedence = precedence
        self.expression = self.FormatExpression()

    def TokenAlphabet(self, alphabet, tokens):
        alphabet = alphabet
        for token in tokens:
            alphabet.append("#" + token)

        return alphabet

    def FormatExpression(self):
        new_expression = self.findExpression()
        # new_expression = self.CheckEpislon(new_expression)
        new_expression = self.AddConcatenation(new_expression)
        return new_expression
    
    def CheckEpislon(self, expression):
        for token in enumerate(expression):
            if token == 'e' or token == 'ϵ':
                expression.replace(token, 'ε')

        return expression

    def AddConcatenation(self, expression):
        new_expr = []
        for i, token in enumerate(expression):
            if i > 0:
                if token in self.alphabet and expression[i-1] in self.alphabet:
                    new_expr.append("•")
                elif token in self.alphabet and expression[i-1] == ')':
                    new_expr.append("•")
                elif token == '(' and expression[i-1] in self.alphabet:
                    new_expr.append("•")
                elif token == '(' and expression[i-1] == ')':
                    new_expr.append("•")
                elif expression[i-1] == '?' and (token in self.alphabet or token == '('):
                    new_expr.append("•")
                elif expression[i-1] == '*' and (token in self.alphabet or token == '('):
                    new_expr.append("•")
                elif expression[i-1] == '+' and (token in self.alphabet or token == '('):
                    new_expr.append("•")
            new_expr.append(token)
           
        print(new_expr)
        return new_expr

    def ValidateExpression(self):

        for token in self.expression:
            if token not in self.alphabet and token not in self.operators:
                if token.startswith('#'):
                    continue
                else:
                    raise ValueError("Caracter invalido: " + token)

        if self.expression.count('(') != self.expression.count(')'):
            raise ValueError("Parentesis sin cerrar")

        for i, token in enumerate(self.expression):
            if token == ')':
                if self.expression[i-1] == '(':
                    raise ValueError("Parentesis vacio")

        for i, token in enumerate(self.expression):
            if token in "|•" and token != '(' and token != ')':
                if i == 0 or i == len(self.expression)-1:
                    raise ValueError("Operador binario no puede estar al inicio o al final")
       
        for i, token in enumerate(self.expression):
            if token in "+*?":
                if self.expression[i-1] not in self.alphabet and self.expression[i-1] != ')' and self.expression[i-1] not in "+*?":
                    raise ValueError("Operador unario debe tener un caracter o ) a la izquierda")

        for i, token in enumerate(self.expression):
            if token in "•|":
                if self.expression[i-1] not in self.alphabet and not self.expression[i-1].startswith('#') and self.expression[i-1] != ')' and self.expression[i-1] not in "+*?":
                    raise ValueError("Operador binario debe tener un caracter o ) a la izquierda")
                if self.expression[i+1] not in self.alphabet and not self.expression[i+1].startswith('#') and self.expression[i+1] != '(' and self.expression[i+1] not in "+*?":
                    raise ValueError("Operador binario debe tener un caracter o ( a la derecha")

        for i, token in enumerate(self.expression):
            if token in "+*?":
                if i == 0:
                    raise ValueError("Operador unario no puede estar al principio")

    def ConvertToPostfix(self):

        try:
            self.ValidateExpression()

        except ValueError as e:
            print(e)
            return None

        stack = []
        postfix = []

        for token in self.expression:
            if token in self.alphabet or token.startswith('#'):
                postfix.append(token) 
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()
            else:
                while stack and self.precedence[token] <= self.precedence[stack[-1]]:
                    postfix.append(stack.pop())
                stack.append(token)

        while stack:
            postfix+=stack.pop()

        return postfix

    def findExpression(self):
        expresiones = []
        temp = ""

        token = False
        tokenString = ""

        for i in range(len(self.expression)):
            
            current = self.expression[i]

            #si es # 
            if current == '"':
                if tokenString != "":
                    expresiones.append(tokenString.replace('"', ''))
                    tokenString = ""
                    token = False
                    continue
                else:
                    token = True

            if token:
                tokenString += current

            else:
            #si es un operador

                if current == "+" or current == "*" or current == "?" or current == "•" or current == "|" or current == "(" or current == ")":
                    if(temp != ""):
                        expresiones.append(temp)
                        temp = ""
                    expresiones.append(current)

                #si es un caracter
                else:
                    temp += current

        if(tokenString != ""):
            expresiones.append(tokenString)

        return expresiones
