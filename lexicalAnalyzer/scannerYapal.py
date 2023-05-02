class ScannerYapal:
    def __init__(self, filename):
        self.filename = filename
        self.tokens = []
        self.productions = {}

    def scan(self):
        with open(self.filename, 'r') as f:
            content = f.read()

        is_parsing_tokens = False
        token = ''
        production = ''

        for symbol in content:
            # parsing tokens =====================================================================
            if is_parsing_tokens:

                if symbol == '%':
                    is_parsing_tokens = False

                elif symbol == '\n':

                    if 'token' in token:
                        token = token.split(' ', 1)[1]

                        if " " in token:

                            for t in token.split(" "):
                                t = t.strip()
                                if "/*" in t and "*/" in t:
                                    start_index = t.index("/*")
                                    end_index = t.index("*/", start_index) + 2
                                    t = t[:start_index] + t[end_index:]
                                self.tokens.append(t)

                        else:

                            if "/*" in token and "*/" in token:
                                start_index = token.index("/*")
                                end_index = token.index("*/", start_index) + 2
                                token = token[:start_index] + token[end_index:]
                            self.tokens.append(token.strip())

                        token = ''
                        is_parsing_tokens = False

                    else:
                        raise Exception('Error en la declaracion de tokens', token)
                    
                else:
                    token += symbol

            # parsing productions =================================================================
            else:
                if symbol == ";":
                    if "/*" in production and "*/" in production:
                        start_index = production.index("/*")
                        end_index = production.index("*/", start_index) + 2
                        production = production[:start_index] + production[end_index:]

                    production = production.split(':')
                    lhs = production[0].strip()
                    rhs = [p.strip() for p in production[1].split("|")]

                    self.productions[lhs] = rhs if len(rhs) > 1 else rhs[0]
                    production = ''
                    
                else:
                    if symbol == '%':
                        is_parsing_tokens = True
                    else:
                        production += symbol

        print(self.tokens)
        print(self.productions)
