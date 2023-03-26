from utils.simbolo import Simbolo

class Scanner:
    def __init__(self, filename):
        self.filename = filename
        self.variables = {}
        self.tokens = {}
        self.rule_tokens = False
        self.final_regex = ""
        self.alphabet = [chr(i) for i in range(256)] # ASCII
        
    def scan(self):
        #leer el archivo
        with open(self.filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            # Ignorar lineas en blanco
            if not line.strip():
                continue

            # Si encuentra un let, guardar la palabra siguiente como llave
            # del diccionario y lo siguiente al = como valor
            if 'let' in line:
                key_value = line.split('=')
                key = key_value[0].strip().split()[1]
                value = key_value[1].strip()
                self.variables[key] = value
                continue

            # Al llegar a "rule tokens ="
            # Se empieza a guardar los tokens
            if 'rule tokens =' in line:
                self.rule_tokens = True
                continue

            if self.rule_tokens:

                temporary_word = ""
                temporary_fun = ""
                fun = False
                in_comment = False

                for i, x in enumerate(line):

                    # Verificar si estamos dentro de un comentario
                    if x == "(" and i < len(line) - 1 and line[i+1] == "*":
                        in_comment = True
                    elif x == "*" and i < len(line) - 1 and line[i+1] == ")":
                        in_comment = False
                        continue  # Ignorar el segundo caracter del comentario

                    # Ignorar los caracteres si estamos dentro de un comentario
                    if in_comment:
                        continue

                    if x != " "  and x != "\t" and x != "\n" and x != "'" and x != "|":
                        if x == "{":
                            fun = True
                        elif x == "}":
                            temporary_fun += x
                            break
                        
                        if fun:
                            temporary_fun += x
                        else:
                            temporary_word += x

                self.tokens[temporary_word] = temporary_fun

           
        
        #agregar concatenaciones necesarias
        self.addConcatenation()

        # reemplazo recursivo de variables
        for key, value in self.variables.items():
            self.variables[key] = self.recursiveSerach(value) 
      
        #armar la expresion final 
        for key, value in self.tokens.items():
            if key in self.variables.keys():
                self.final_regex += self.variables[key] + "|"
            else:
                self.final_regex += str(Simbolo(key)) + "|"

        self.final_regex = self.final_regex[:-1]


    def getRegex(self, value):

        if "-" in value:
            value = value.replace("'", "")

            temp = ""
            for i, x in enumerate(value):
                if x == "|" or x == "•" or x == "*" or x == "+" or x == "?":
                    temp += x

                if x == "-":
                    first = value[i-1]
                    last = value[i+1]


                    for j in range(ord(first), ord(last)+1):
                        temp += str(j) + "|"

            return ("(" + temp[:-1] + ")")

        else:
            tempTotal = ""
            temp = ""
            openComilla = False

            for i, x in enumerate(value):
                if x == "'":
                    if temp != "":
                        if temp == "\\t":
                            tempTotal += "9" + "|"

                        elif temp == "\\n":
                            tempTotal += "10" + "|"

                        else:
                            tempTotal += str(ord(temp)) + "|"
                            
                        temp = ""
                    openComilla = not openComilla
                    continue

                if openComilla:
                    temp += x

            return ("(" + tempTotal[:-1] + ")")


    def recursiveSerach(self, value):
        if(value.startswith('[')):
            return self.getRegex(value)
        
        elif value in self.variables.keys():
            return self.variables[value]
        
        if value in self.alphabet:
            return str(ord(value))
  
        else:

            if '(' in value:    
                #enviar lo que este entre () a la funcion recursiva
                temp = ("(" + self.recursiveSerach(value.split('(')[1].split(')')[0]) + ")")

                # si hay algo antes de los parentesis
                if value.split('(')[0]:
                    temp = self.recursiveSerach(value.split('(')[0][:-1]) + value.split('(')[0][-1] + temp
                
                # si hay algo despues de los parentesis
                if value.split(')')[1]:

                    if(value.split(')')[1].startswith('|')  or value.split(')')[1].startswith('.')):
                        temp = temp + self.recursiveSerach(value.split(')')[1][:-1]) + value.split(')')[1][-1]

                    else:
                        temp = temp + value.split(')')[1] 

                return temp
                   

            if "|" in value:
                return(self.recursiveSerach(value.split('|')[0]) + "|" + self.recursiveSerach(value.split('|')[1]))
            
            elif '•' in value:
                return(self.recursiveSerach(value.split('.')[0]) + "•" + self.recursiveSerach(value.split('.')[1]))

            if '+' in value:
                return(self.recursiveSerach(value.split('+')[0]) + "+")
            
            elif '*' in value:
                return(self.recursiveSerach(value.split('*')[0]) + "*")
            
            elif '?' in value:
                return(self.recursiveSerach(value.split('?')[0]) + "?")
            
            elif '|' in value:
                return(self.recursiveSerach(value.split('|')[0]) + "|" + self.recursiveSerach(value.split('|')[1]))
            
            else:
                before = ""
                match ="" 
                after= ""
                temp = ""
                keys_ordered = sorted(self.variables.keys(), key=len, reverse=True)

                for key in keys_ordered:
                    if key in value:
                        before, match, after = value.partition(key)
                        match = self.recursiveSerach(match)
                        value = value.replace(key, "")     

                        if before != "":
                            before = self.recursiveSerach(before)
                            value = value.replace(before, "") 

                        if after != "":
                            after = self.recursiveSerach(after) 
                            value = value.replace(after, "") 

                        temp = "(" + before + match + after + ")"
          
                return temp            


    def addConcatenation(self):
        for key, value in self.variables.items():
            
            if not value.startswith('['):

                expresiones = []
                temp = ""
                for i, x in enumerate(value):
                    if x == "+" or x == "*" or x == "?"  or x == "|" or x == "(" or x == ")":
                        if(temp != ""):
                            expresiones.append(temp)
                            temp = ""
                        expresiones.append(x)

                    else:
                        temp += x

                if(temp != ""):
                    expresiones.append(temp)

                new_expr = []
                for i, token in enumerate(expresiones):
                    if i > 0:
                        if token in self.variables.keys() and expresiones[i-1] in self.variables.keys():
                            new_expr.append("•")
                        elif token in self.variables.keys() and expresiones[i-1] == ')':
                            new_expr.append("•")
                        elif token == '(' and expresiones[i-1] in self.variables.keys():
                            new_expr.append("•")
                        elif token == '(' and expresiones[i-1] == ')':
                            new_expr.append("•")
                        elif expresiones[i-1] == '?' and (token in self.variables.keys() or token == '('):
                            new_expr.append("•")
                        elif expresiones[i-1] == '*' and (token in self.variables.keys() or token == '('):
                            new_expr.append("•")
                        elif expresiones[i-1] == '+' and (token in self.variables.keys() or token == '('):
                            new_expr.append("•")
                    new_expr.append(token)

                self.variables[key] = ''.join(new_expr)
