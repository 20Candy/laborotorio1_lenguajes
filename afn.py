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
            estado_final = Estado(self.contador + 1, 'final')
            self.agregar_estado(estado_inicial)
            self.agregar_estado_final(estado_final)
            self.agregar_simbolo(nodo.simbolo)
            self.agregar_transicion(estado_inicial, estado_final, nodo.simbolo)
            self.estado_inicial = estado_inicial
            self.contador += 1
            return self
            
        if nodo.simbolo == '|':
            fragmento_izquierdo = self.Thompson(nodo.hijo_izq)
            fragmento_derecho = self.Thompson(nodo.hijo_der)

            #unir los fragmentos mediante una transición epsilon y retornar el nuevo autómata
            estado_inicial = Estado(self.contador, 'normal')
            estado_final = Estado(self.contador + 1, 'final')
            self.agregar_estado(estado_inicial)
            self.agregar_estado_final(estado_final)
            self.agregar_simbolo('epsilon')
            self.agregar_transicion(estado_inicial, fragmento_izquierdo.estado_inicial, 'epsilon')
            self.agregar_transicion(estado_inicial, fragmento_derecho.estado_inicial, 'epsilon')
            self.agregar_transicion(fragmento_izquierdo.EstadosFinales.PopItem(), estado_final, 'epsilon')
            self.agregar_transicion(fragmento_derecho.EstadosFinales.PopItem(), estado_final, 'epsilon')
            self.estado_inicial = estado_inicial
            self.contador += 1
            return self


        if nodo.simbolo == '.':
            fragmento_izquierdo = self.Thompson(nodo.hijo_izq)
            fragmento_derecho = self.Thompson(nodo.hijo_der)
            #crear un nuevo estado inicial y final, con transiciones epsilon hacia los estados iniciales de los fragmentos y desde los estados finales de los fragmentos hacia el nuevo estado final. Retornar el nuevo autómata
            estado_inicial = Estado(self.contador, 'normal')
            estado_final = Estado(self.contador + 1, 'final')
            self.agregar_estado(estado_inicial)
            self.agregar_estado_final(estado_final)
            self.agregar_simbolo('epsilon')
            self.agregar_transicion(estado_inicial, fragmento_izquierdo.estado_inicial, 'epsilon')
            self.agregar_transicion(estado_inicial, fragmento_derecho.estado_inicial, 'epsilon')
            self.agregar_transicion(fragmento_izquierdo.EstadosFinales.PopItem(), estado_final, 'epsilon')
            self.agregar_transicion(fragmento_derecho.EstadosFinales.PopItem(), estado_final, 'epsilon')
            self.estado_inicial = estado_inicial
            self.contador += 1
            return self
        
        if nodo.simbolo == '?':
            fragmento_izquierdo = self.Thompson(nodo.hijo_izq)
            # crear un nuevo estado inicial y final, con transiciones epsilon hacia el estado inicial del fragmento y desde el estado final del fragmento hacia el nuevo estado final. Añadir una transición epsilon directa desde el nuevo estado inicial hacia el nuevo estado final. Retornar el nuevo autómata
            estado_inicial = Estado(self.contador, 'normal')
            estado_final = Estado(self.contador + 1, 'final')
            self.agregar_estado(estado_inicial)
            self.agregar_estado_final(estado_final)
            self.agregar_simbolo('epsilon')
            self.agregar_transicion(estado_inicial, fragmento_izquierdo.estado_inicial, 'epsilon')
            self.agregar_transicion(fragmento_izquierdo.EstadosFinales.PopItem(), estado_final, 'epsilon')
            self.agregar_transicion(estado_inicial, estado_final, 'epsilon')
            self.estado_inicial = estado_inicial
            self.contador += 1
            return self

        if nodo.simbolo == '*':
            fragmento_izquierdo = self.Thompson(nodo.hijo_izq)
            #crear un nuevo estado inicial y final, con transiciones epsilon hacia el estado inicial del fragmento y desde el estado final del fragmento hacia el nuevo estado final. Añadir transiciones epsilon desde el nuevo estado inicial hacia el nuevo estado final y desde el nuevo estado final hacia el nuevo estado inicial. Retornar el nuevo autómata
            estado_inicial = Estado(self.contador, 'normal')
            estado_final = Estado(self.contador + 1, 'final')
            self.agregar_estado(estado_inicial)
            self.agregar_estado_final(estado_final)
            self.agregar_simbolo('epsilon')
            self.agregar_transicion(estado_inicial, fragmento_izquierdo.estado_inicial, 'epsilon')
            self.agregar_transicion(fragmento_izquierdo.EstadosFinales.PopItem(), estado_final, 'epsilon')
            self.agregar_transicion(estado_inicial, estado_final, 'epsilon')
            self.agregar_transicion(estado_final, estado_inicial, 'epsilon')
            self.estado_inicial = estado_inicial
            self.contador += 1
            return self


        if nodo.simbolo == '+':
            fragmento_izquierdo = self.Thompson(nodo.hijo_izq)
            #crear un nuevo estado inicial y final, con transiciones epsilon hacia el estado inicial del fragmento y desde el estado final del fragmento hacia el nuevo estado final. Añadir transiciones epsilon desde el nuevo estado inicial hacia el nuevo estado final y desde el estado final del fragmento hacia el estado inicial del fragmento. Retornar el nuevo autómata
            estado_inicial = Estado(self.contador, 'normal')
            estado_final = Estado(self.contador + 1, 'final')
            self.agregar_estado(estado_inicial)
            self.agregar_estado_final(estado_final)
            self.agregar_simbolo('epsilon')
            self.agregar_transicion(estado_inicial, fragmento_izquierdo.estado_inicial, 'epsilon')
            self.agregar_transicion(fragmento_izquierdo.EstadosFinales.PopItem(), estado_final, 'epsilon')
            self.agregar_transicion(estado_inicial, estado_final, 'epsilon')
            self.agregar_transicion(estado_final, fragmento_izquierdo.estado_inicial, 'epsilon')
            self.estado_inicial = estado_inicial
            self.contador += 1
            return self


        

    def cerradura_epsilon(self, conjunto_estados):
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
        conjunto_estados = self.cerradura_epsilon(self.estado_inicial.EstadosAFN)
        for simbolo in cadena:
            conjunto_estados = self.mover(conjunto_estados, simbolo)
            conjunto_estados = self.cerradura_epsilon(conjunto_estados)
        for estado in conjunto_estados.Elementos:
            if estado in self.EstadosFinales.Elementos:
                return True
        return False    


    def graficar(self, nombre_archivo):
        from graphviz import Digraph

        g = Digraph('AFN', filename=nombre_archivo)

        # Agregar los estados al grafo
        for estado in self.Estados.Elementos:
            if estado in self.EstadosFinales.Elementos:
                g.node(str(estado.id), label=str(estado.id), shape='doublecircle')
            else:
                g.node(str(estado.id), label=str(estado.id), shape='circle')

        # Agregar las transiciones al grafo
        for transicion in self.transiciones:
            g.edge(str(transicion[0].id), str(transicion[1].id), label=transicion[2])

        g.view()


