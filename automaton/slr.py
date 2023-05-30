from automaton.automaton import Automaton
from utils.state import State
from utils.set import Set

from prettytable import PrettyTable

class SLR(Automaton):
    def __init__(self, tokens, productions, ignore):
        self.terminals = tokens
        self.grammar = productions
        self.ignore = ignore
        self.symbols = Set()
        self.producciones = self.formatSLR()
        self.initialState = None
        self.states = Set()
        self.transitions = []
        self.finalStates = Set()
        self.start = None
        self.action_table = [[]]
        self.goto_table = [[]]
        self.contador = 0

    def SLR(self,):
        #estado inicial es la primera produccion de self.producciones que no es un terminal
        for produccion in self.producciones:
            if produccion.split("=>")[0] not in self.terminals:
                
                #agregar puntito al inicio de la produccion
                produccion = produccion.split("=>")
                produccion[1] = " ." + produccion[1]
                produccion = produccion[0] + "=>" + produccion[1]
                self.start = produccion
                cerradura  = self.cerradura(produccion)
                self.initialState = State("\n".join(cerradura), "inicial", None, self.contador, self.cerradura(produccion))
                break

    
        #agregar estado inicial a la lista de estados
        self.states.AddItem(self.initialState)
        self.contador += 1

        #recorrer estados
        for estado in self.states.elements:
            for symbol in self.symbols.elements:
                #obtener el estado siguiente
                siguiente = self.ir_a(estado, symbol)
                if siguiente != None:
                    #si el estado siguiente no esta en la lista de estados

                    if self.verificarRepetidos(siguiente) == False:
                        #agregar el estado a la lista de estados
                        siguiente.token = self.contador
                        self.states.AddItem(siguiente)
                        self.contador += 1

                        #verificar si el estado siguiente es un estado final
                        if siguiente.type == "final":
                            self.finalStates.AddItem(siguiente)
                    else:
                        for estado1 in self.states.elements:
                            if siguiente.productions == estado1.productions:
                                siguiente.token = estado1.token
                    
                    #agregar transicion
                    self.addTransition(estado, siguiente, symbol)


        self.toString()
        self.toGraph(self, "SLR")


    def ir_a(self,estado,simbolo):
        producciones = []
        for produccion in estado.productions:

            if produccion.split("=>")[1].split(".")[1].split().__len__() > 0:

                if produccion.split("=>")[1].split(".")[1].split()[0].strip() == simbolo:

                    antes, despues = produccion.split(".")
                    despues = despues.split()

                    if len(despues) == 1:
                        produccion = antes + " " + despues[0] + " ."
                    
                    else:
                        produccion = antes + " " + despues[0] + " . " + " ".join(despues[1:])
                    producciones.append(produccion)
            
        for produccion in producciones:
            #si el puntito esta a la izquierda de un no terminal
            if produccion.split(".")[1].split().__len__() > 0:
                right_part = produccion.split(".")[1].split()[0].strip()
            
                if right_part not in self.terminals and right_part != "=>":
                    cerradura = self.cerradura(produccion)

                    for produccion in cerradura:
                        if produccion not in producciones:
                            producciones.append(produccion)

        if len(producciones) > 0:
            # si tiene una produccion del estado inical pero con el puntito al final

            for produccion in producciones:
                if produccion.replace(".", "").strip() == self.start.replace(".", "").strip():
                    right_part_InitState = self.start.split(".")[1].split()[0].strip()
                    left_part_produccion = produccion.split(".")[0].split()[-1].strip()

                    if right_part_InitState == left_part_produccion:


                        return State("\n".join(producciones), "final", None, None, producciones)
            else:

                return State("\n".join(producciones), "normal", None, None, producciones)
        
        else:
            return None

    def cerradura(self,produccion):
        producciones = []
        producciones.append(produccion)

        for produccion1 in producciones:
            for produccion2 in self.producciones:
                term1 = produccion1.split("=>")[1].split(".")[1].split()[0].strip()
                term2 = produccion2.split("=>")[0].strip()
                if term1 == term2:
                    produccion2 = produccion2.split("=>")
                    produccion2[1] = " ." + produccion2[1]
                    produccion2 = produccion2[0] + "=>" + produccion2[1]
                    
                    if produccion2 not in producciones:
                        producciones.append(produccion2)
        return producciones


    def formatSLR(self):
        grammar_array = []

        #gramatica aumentada
        key = list(self.grammar.keys())[0]
        grammar_array.append(key + "'" + ' => ' + key)

        self.symbols.AddItem(key)

        for nonterminal, productions in self.grammar.items():
            for production in productions:

                for word in production.split(' '):
                    if word not in self.symbols.elements:
                        self.symbols.AddItem(word)

                grammar_array.append(nonterminal + ' => ' + production)

        return grammar_array
    
    def verificarRepetidos(self, siguiente):
        for estado in self.states.elements:
            if siguiente.productions == estado.productions:
                return True

        return False
              
    def calcular_primero(self, simbolo):
        primero = set()
        if simbolo in self.terminals:
            primero.add(simbolo)
            return primero
        for produccion in self.grammar[simbolo]:
            primer_simbolo = produccion.split()[0]
            if primer_simbolo in self.terminals:
                primero.add(primer_simbolo)
            elif primer_simbolo != simbolo:
                conjunto_primero = self.calcular_primero(primer_simbolo)
                primero.update(conjunto_primero)
            else:
                continue
        return primero


    def calcular_siguiente(self, simbolo):
        siguiente = set()
        if simbolo == list(self.grammar.keys())[0]:
            siguiente.add('$')
        for no_terminal in self.grammar:
            for produccion in self.grammar[no_terminal]:
                if simbolo in produccion:
                    lista = produccion.split()
                    simbolo_index = lista.index(simbolo)

                    if simbolo_index == len(lista) - 1:
                        if no_terminal != simbolo:
                            conjunto_siguiente = self.calcular_siguiente(no_terminal)
                            siguiente.update(conjunto_siguiente)
                    else:
                        siguiente_simbolo = lista[simbolo_index+1]
                        conjunto_primero = self.calcular_primero(siguiente_simbolo)
                        if 'ε' in conjunto_primero:
                            if no_terminal != simbolo:
                                conjunto_siguiente = self.calcular_siguiente(no_terminal)
                                siguiente.update(conjunto_siguiente)
                            conjunto_primero.remove('&')
                        siguiente.update(conjunto_primero)
        return siguiente
    
    def tabla(self):
        # obtener símbolos terminales y no terminales
        simbolos_terminales = self.terminals + ['$']
        simbolos_no_terminales = self.symbols.Difference(Set(simbolos_terminales))

        #quitar los que esten en ignore
        for s in simbolos_terminales:
            if s in self.ignore:
                simbolos_terminales.remove(s)

        # inicializar la tabla go_to como una matriz vacía
        go_to_table = [[None] * len(simbolos_no_terminales) for _ in range(self.states.__len__())]

        # llenar la tabla go_to
        for transicion in self.transitions:
            if transicion[2] in simbolos_no_terminales.elements:
                simbolo = simbolos_no_terminales.elements.index(transicion[2])
                go_to_table[transicion[0].token][simbolo] = transicion[1].token

        self.goto_table = go_to_table

        # inicializar la tabla action como una matriz vacía
        action_table = [[None] * len(simbolos_terminales) for _ in range(self.states.__len__())]

        # llenar la tabla action con los shift
        for transicion in self.transitions:
            if transicion[2] in simbolos_terminales:
                simbolo = simbolos_terminales.index(transicion[2])
                action_table[transicion[0].token][simbolo] = "S" + (transicion[1].token).__str__()

        # llenar la tabla con accept
        for i in range(1, self.states.__len__()):
            estado = self.states.elements[i]
            for produccion in estado.productions:
                if produccion.replace(".", "").strip() == self.start.replace(".", "").strip():
                    simbolo = simbolos_terminales.index("$")
                    action_table[estado.token][simbolo] = "ACCEPT"
                    i = self.states.__len__()
                    break


        # Llenar la tabla con reduce
        for i in range(self.states.elements.__len__()):
            estado = self.states.elements[i]
            for produccion in estado.productions:
                if produccion.endswith('.'):
                    simbolos = produccion.split('=>')[0]
                    simbolos_no_espacios = simbolos.replace(' ', '')
                    follow = self.calcular_siguiente(simbolos_no_espacios)

                    for simbolo in follow:
                        if simbolo in simbolos_terminales:
                            simbolo_index = simbolos_terminales.index(simbolo)
                            if action_table[estado.token][simbolo_index] is None:
                                action_table[estado.token][simbolo_index] = "R" + self.buscarEstado(produccion).__str__()
                            else:
                                raise Exception("Error en la tabla de accion")
                            
        self.action_table = action_table

        # Imprimir la tabla de Acción
        print("\nTabla de Acción:")
        headers = simbolos_terminales
        accion_table = PrettyTable(headers)
        for i in range(self.states.__len__()):
            accion_table.add_row(action_table[i])
        print(accion_table)

        # Imprimir la tabla de Goto
        print("\nTabla de Goto:")
        headers = simbolos_no_terminales.elements
        goto_table = PrettyTable(headers)
        for i in range(self.states.__len__()):
            goto_table.add_row(go_to_table[i])
        print(goto_table)


    def buscarEstado(self, produccion):
        for i in range(self.initialState.productions.__len__()):
            p = self.initialState.productions[i]
            if produccion.replace(".", "").strip().replace(" ","") == p.replace(".", "").strip().replace(" ",""):
                return i

    def simulacion(self, cadena):
        stack = [self.initialState]  # Pila de estados
        input_symbols = cadena.split()  # Símbolos de entrada

        while True:
            state = stack[-1]  # Estado en la cima de la pila
            symbol = input_symbols[0]  # Siguiente símbolo de entrada

            # Obtener la acción correspondiente al estado y símbolo actual
            action = self.action_table[state.token][self.terminals.index(symbol)]

            if action.startswith("S"):  # Shift
                next_state = self.states.GetItem(int(action[1:]))
                stack.append(next_state)
                input_symbols = input_symbols[1:]  # Avanzar al siguiente símbolo de entrada
            elif action.startswith("R"):  # Reduce
                production_index = int(action[1:])
                production = self.producciones[production_index]

                left_part, right_part = production.split("=>")
                right_part_symbols = right_part.split()
                num_symbols_to_pop = len(right_part_symbols)

                for _ in range(num_symbols_to_pop):
                    stack.pop()

                next_state = stack[-1]
                goto_action = self.goto_table[next_state.token][self.symbols.elements.index(left_part)]

                stack.append(State("\n".join(production), "normal", None, None, production.splitlines()))
                stack.append(self.states.GetItem(goto_action))
            elif action == "ACCEPT":  # Aceptación
                return "YES"
            else:
                return "NO"  # La cadena no es aceptada

        return "NO"  # La cadena no es aceptada

        
