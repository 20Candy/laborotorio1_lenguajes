class Scanner:
    def __init__(self, filename):
        self.filename = filename
        self.variables = {}
        self.tokens = {}
        self.rule_tokens = True
        
    def scan(self):
        #leer el archivo
        with open(self.filename, 'r') as f:
            lines = f.readlines()

        ignore_block_comment = False
        for line in lines:
            # Ignorar lo que este entre (* *)
            if '(*' in line:
                ignore_block_comment = True
            if ignore_block_comment and '*)' in line:
                ignore_block_comment = False
                continue
            if ignore_block_comment:
                continue

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

                for x in line:

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

    def __str__(self):
        return f'Tokens: {self.tokens}\nVariables: {self.variables}'
