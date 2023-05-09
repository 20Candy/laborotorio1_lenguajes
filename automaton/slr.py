from automaton.automaton import Automaton
from utils.state import State
from utils.set import Set


class SLR(Automaton):
    def __init__(self, tokens, productions):
        self.terminals = tokens
        self.grammar = productions
        self.symbols = Set()
        self.producciones = self.formatSLR()
        self.initialState = None
        self.states = Set()
        self.transitions = []
        self.finalStates = Set()
        self.start = None
        self.primeroList = []


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
                self.initialState = State("\n".join(cerradura), "inicial", None, None, self.cerradura(produccion))
                break

    
        #agregar estado inicial a la lista de estados
        self.states.AddItem(self.initialState)

        #recorrer estados
        for estado in self.states.elements:
            for symbol in self.symbols.elements:
                #obtener el estado siguiente
                siguiente = self.ir_a(estado, symbol)
                if siguiente != None:
                    #si el estado siguiente no esta en la lista de estados

                    if self.verificarRepetidos(siguiente) == False:
                        #agregar el estado a la lista de estados
                        self.states.AddItem(siguiente)

                        #verificar si el estado siguiente es un estado final
                        if siguiente.type == "final":
                            self.finalStates.AddItem(siguiente)

                    #agregar transicion
                    self.addTransition(estado, siguiente, symbol)

        self.pruebas()

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
                if produccion.replace(".", "").replace(" ", "") == self.start.replace(".", "").replace(" ", ""):
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

        
    def pruebas(self):

        for key, value in self.grammar.items():
            rightpart = key
            self.primeroList = []
            self.primero(rightpart)
            print("primero de " + rightpart + " es: " + str(self.primeroList))


    def primero(self, rightpart):
        for key, value in self.grammar.items():
            if key.strip() == rightpart.strip():
                pruducciones = value
                for produccion in pruducciones:

                    if not produccion.split()[0].strip() == rightpart.strip():
                        if produccion.split()[0].strip() in self.terminals:
                            self.primeroList.append(produccion.split()[0])
                        else:
                            self.primero(produccion.split()[0])

    
        