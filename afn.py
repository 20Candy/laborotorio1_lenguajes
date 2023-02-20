from automata import Automata
from estado import Estado
from transicion import Transicion

from graphviz import Digraph

class AFN(Automata):
    def __init__(self):
        super().__init__()
        self.contador = 0


    def Thompson(self, nodo):

        #si simbolo terminal
        if nodo.hijo_izq is None and nodo.hijo_der is None:
            #crear un nuevo estado inicial y la transicion que coreesponde
            
            estado_inicial = Estado(self.contador, 'normal')
            estado_destino = Estado(self.contador + 1, 'normal')
            self.contador += 1
            self.agregar_transicion(estado_inicial, estado_destino, nodo.simbolo)
            
            self.agregar_estado_final(estado_destino)
            self.agregar_simbolo(nodo.simbolo)
            self.estado_inicial = estado_inicial

            return self
            
        if nodo.simbolo == '|':

            estado1 = Estado(self.contador, 'normal')
            self.agregar_estado(estado1)
            self.contador += 1
            fragmento_izquierdo = self.Thompson(nodo.hijo_izq)
            self.agregar_transicion(estado1, fragmento_izquierdo.estado_inicial, 'ε') 
            
            
            estado2 = Estado(self.contador + 1, 'normal')
            self.agregar_estado(estado2)
            self.contador += 1
            fragmento_derecho = self.Thompson(nodo.hijo_der)
            self.agregar_transicion(estado1, fragmento_derecho.estado_inicial, 'ε')


            # si hay mas de un estado final, agregar un estado y transiciones epsilon desde los estados finales hacia el nuevo estado final
            if len(self.EstadosFinales.Elementos) > 1:
                estados_finales = self.EstadosFinales.Elementos
                self.cleanEstadoFinal()
                estado_final = Estado(self.contador +1, 'final')
                self.agregar_estado_final(estado_final)
                self.agregar_simbolo('ε')
                for estado in estados_finales:
                    self.agregar_transicion(estado, estado_final, 'ε')
                self.contador += 1

            self.estado_inicial = estado1
            self.agregar_simbolo('ε')
            
            return self


        if nodo.simbolo == '.':       

            estado1 = Estado(self.contador, 'normal')
            fragmento_izquierdo = self.Thompson(nodo.hijo_izq)
            fragmento_derecho = self.Thompson(nodo.hijo_der)

            self.estado_inicial = estado1

            return self
        
        if nodo.simbolo == '?':
            fragmento_izquierdo = self.Thompson(nodo.hijo_izq)
            # crear un nuevo estado inicial y final, con transiciones ε hacia el estado inicial del fragmento y desde el estado final del fragmento hacia el nuevo estado final. Añadir una transición ε directa desde el nuevo estado inicial hacia el nuevo estado final. Retornar el nuevo autómata
            estado_inicial = Estado(self.contador, 'normal')
            estado_final = Estado(self.contador + 1, 'final')
            self.agregar_estado(estado_inicial)
            self.agregar_estado_final(estado_final)
            self.agregar_simbolo('ε')
            self.agregar_transicion(estado_inicial, fragmento_izquierdo.estado_inicial, 'ε')
            self.agregar_transicion(fragmento_izquierdo.EstadosFinales.PopItem(), estado_final, 'ε')
            self.agregar_transicion(estado_inicial, estado_final, 'ε')
            self.estado_inicial = estado_inicial
            self.contador += 1
            return self

        if nodo.simbolo == '*':

            estado_inicial = Estado(self.contador, 'normal')
            estado_destino = Estado(self.contador + 1, 'normal')
            self.contador += 1
            self.agregar_simbolo('ε')
            self.agregar_transicion(estado_inicial, estado_destino, 'ε')

            fragmento_izquierdo = self.Thompson(nodo.hijo_izq)
            estado_final_izquierdo = fragmento_izquierdo.EstadosFinales.Elementos[-1]

            estado_final = Estado(self.contador + 1, 'final')
            self.agregar_estado_final(estado_final)
            self.contador += 1

            self.agregar_transicion(estado_final_izquierdo, estado_final, 'ε')
            self.agregar_transicion(estado_inicial, estado_final, 'ε')
            self.agregar_transicion(estado_final_izquierdo, estado_destino, 'ε')

            
            
            self.estado_inicial = estado_inicial
           
            return self


        if nodo.simbolo == '+':
            fragmento_izquierdo = self.Thompson(nodo.hijo_izq)
            #crear un nuevo estado inicial y final, con transiciones ε hacia el estado inicial del fragmento y desde el estado final del fragmento hacia el nuevo estado final. Añadir transiciones ε desde el nuevo estado inicial hacia el nuevo estado final y desde el estado final del fragmento hacia el estado inicial del fragmento. Retornar el nuevo autómata
            estado_inicial = Estado(self.contador, 'normal')
            estado_final = Estado(self.contador + 1, 'final')
            self.agregar_estado(estado_inicial)
            self.agregar_estado_final(estado_final)
            self.agregar_simbolo('ε')
            self.agregar_transicion(estado_inicial, fragmento_izquierdo.estado_inicial, 'ε')
            self.agregar_transicion(fragmento_izquierdo.EstadosFinales.PopItem(), estado_final, 'ε')
            self.agregar_transicion(estado_inicial, estado_final, 'ε')
            self.estado_inicial = estado_inicial
            self.contador += 1
            return self
         

    def cerradura_ε(self, conjunto_estados):
        conjunto_resultado = conjunto_estados
        for estado in conjunto_estados.Elementos:
            for transicion in self.transiciones:
                if transicion.estado_origen == estado and transicion.el_simbolo == 'ε':
                    conjunto_resultado = conjunto_resultado.Union(transicion.estado_destino.EstadosAFN)
        return conjunto_resultado

    def mover(self, conjunto_estados, simbolo):
        conjunto_resultado = Estado()
        for estado in conjunto_estados.Elementos:
            for transicion in self.transiciones:
                if transicion.estado_origen == estado and transicion.el_simbolo == simbolo:
                    conjunto_resultado = conjunto_resultado.Union(transicion.estado_destino.EstadosAFN)
        return conjunto_resultado

    def evaluar_cadena(self, cadena):
        conjunto_estados = self.cerradura_ε(self.estado_inicial.EstadosAFN)
        for simbolo in cadena:
            conjunto_estados = self.mover(conjunto_estados, simbolo)
            conjunto_estados = self.cerradura_ε(conjunto_estados)
        for estado in conjunto_estados.Elementos:
            if estado in self.EstadosFinales.Elementos:
                return True
        return False    


    def graficar(self, nombre_archivo):

        from graphviz import Digraph

        g = Digraph('AFN', filename=nombre_archivo)

        # Agregar los estados al grafo
        for estado in self.Estados.Elementos:
            if estado.tipo == 'final':
                g.node(str(estado.id), label=str(estado.id), shape='doublecircle')
            else:
                g.node(str(estado.id), label=str(estado.id), shape='circle')

        # Agregar las transiciones al grafo
        for transicion in self.transiciones:
            g.edge(str(transicion[0].id), str(transicion[1].id), label=transicion[2])

        g.view()


