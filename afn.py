from automata import Automata
from estado import Estado
from transicion import Transicion

from graphviz import Digraph

class AFN(Automata):
    def __init__(self):
        super().__init__()
        self.contador = 0

    def construir_afn(self, nodo):
        afn = self.Thompson(nodo)

        if afn is not None:

            #eliminar estados repetidos
            afn.Estados.Elementos = list(set(afn.Estados.Elementos))

            #ordenar estados
            afn.Estados.Elementos.sort(key=lambda x: x.id)

            #agregar estado inicial
            afn.Estados.Elementos[0].tipo = 'inicial'

            #agregar estados finales
            afn.agregar_estado_final(afn.Estados.Elementos[-1])
            afn.Estados.Elementos[-1].tipo = 'final'

        afn.toString()
        afn.graficar(afn,"AFN")

        return afn
            
    def Thompson(self, nodo):

        #si simbolo terminal
        if nodo.hijo_izq is None and nodo.hijo_der is None:

            #crear un afn
            afn = AFN()

            #agregar estado inicial del afn
            afn.estado_inicial = Estado(self.contador, 'normal')
            afn.agregar_estado(afn.estado_inicial)

            #agregar estado final del afn
            estado_final = Estado(self.contador + 1, 'normal')
            afn.setEstadoFinal(estado_final)
            afn.agregar_estado(estado_final)
            
            self.contador += 1

            #agregar transiciones del afn
            afn.agregar_transicion(afn.estado_inicial, estado_final, nodo.simbolo)
            
            #agregar simbolo del afn
            afn.agregar_simbolo(nodo.simbolo)


            return afn
            
        if nodo.simbolo == '|':

            #crear un afn
            afn = AFN()

            #agregar estado inicial del afn
            afn.estado_inicial = Estado(self.contador, 'normal')
            afn.agregar_estado(afn.estado_inicial)
            self.contador += 1

            #afn del hijo izquierdo
            afn_izquierdo = self.Thompson(nodo.hijo_izq)
            afn.agregar_transicion(afn.estado_inicial, afn_izquierdo.estado_inicial, 'ε')
            self.contador += 1

            #afn del hijo derecho
            afn_derecho = self.Thompson(nodo.hijo_der)
            afn.agregar_transicion(afn.estado_inicial, afn_derecho.estado_inicial, 'ε')

            #agregar estado final de |
            estado_final = Estado(self.contador + 1, 'normal')
            afn.setEstadoFinal(estado_final)
            afn.agregar_estado(estado_final)
            self.contador += 1

            #agregar transiciones de los hijos
            afn.agregar_transicion(afn_izquierdo.EstadosFinales.Elementos[-1], estado_final, 'ε')
            afn.agregar_transicion(afn_derecho.EstadosFinales.Elementos[-1], estado_final, 'ε')

            #agregar simbolo del afn
            afn.agregar_simbolo('ε')

            #unir estados del afn actial con el afn de los hijos
            afn.Estados = afn.Estados.Union(afn_izquierdo.Estados)
            afn.Estados = afn.Estados.Union(afn_derecho.Estados)

            #unir simbolos del afn actual con el afn de los hijos
            afn.Simbolos = afn.Simbolos.Union(afn_izquierdo.Simbolos)
            afn.Simbolos = afn.Simbolos.Union(afn_derecho.Simbolos)

            #unir transiciones del afn actual con el afn de los hijos
            afn.transiciones = afn.transiciones + afn_izquierdo.transiciones + afn_derecho.transiciones
                        
            return afn


        if nodo.simbolo == '.':       
            #crear un afn
            afn = AFN()

            #agregar estado inicial del afn
            afn.estado_inicial = Estado(self.contador, 'normal')
            afn.agregar_estado(afn.estado_inicial)
            
            #afn del hijo izquierdo
            afn_izquierdo = self.Thompson(nodo.hijo_izq)

            #afn del hijo derecho
            afn_derecho = self.Thompson(nodo.hijo_der)

            #unir estados del afn actial con el afn de los hijos
            afn.Estados = afn.Estados.Union(afn_izquierdo.Estados)
            afn.Estados = afn.Estados.Union(afn_derecho.Estados)

            #unir simbolos del afn actual con el afn de los hijos
            afn.Simbolos = afn.Simbolos.Union(afn_izquierdo.Simbolos)
            afn.Simbolos = afn.Simbolos.Union(afn_derecho.Simbolos)

            #unir transiciones del afn actual con el afn de los hijos
            afn.transiciones = afn.transiciones + afn_izquierdo.transiciones + afn_derecho.transiciones
                        

            return afn
        
        if nodo.simbolo == '?':

            #crear un afn
            afn = AFN()

            #agregar estado inicial del afn
            afn.estado_inicial = Estado(self.contador, 'normal')
            afn.agregar_estado(afn.estado_inicial)
            self.contador += 1

            #afn del hijo izquierdo
            afn_izquierdo = self.Thompson(nodo.hijo_izq)
            afn.agregar_transicion(afn.estado_inicial, afn_izquierdo.estado_inicial, 'ε')

            #agregar estado intermedio 1
            estado_intermedio1 = Estado(self.contador +1, 'normal')
            afn.agregar_estado(estado_intermedio1)
            self.contador += 1

            #transicion entre estado inicial y estado intermedio
            afn.agregar_transicion(afn.estado_inicial, estado_intermedio1, 'ε')

            #agregar estado intermedio 2
            estado_intermedio2 = Estado(self.contador +1, 'normal')
            afn.agregar_estado(estado_intermedio2)
            self.contador += 1

            #transicion entre estado intermedio 1 y estado intermedio 2
            afn.agregar_transicion(estado_intermedio1, estado_intermedio2, 'ε')
            
            #agregar estado final de ?
            estado_final = Estado(self.contador + 1, 'normal')
            afn.setEstadoFinal(estado_final)
            afn.agregar_estado(estado_final)
            self.contador += 1

            #agregar transiciones de los hijos
            afn.agregar_transicion(afn_izquierdo.EstadosFinales.Elementos[-1], estado_final, 'ε')
            afn.agregar_transicion(estado_intermedio2, estado_final, 'ε')

            #agregar el nuevo estado final al hijo izquierdo
            afn_izquierdo.setEstadoFinal(estado_final)

            #agregar simbolo del afn
            afn.agregar_simbolo('ε')

            #unir estados del afn actial con el afn de los hijos
            afn.Estados = afn.Estados.Union(afn_izquierdo.Estados)

            #unir simbolos del afn actual con el afn de los hijos
            afn.Simbolos = afn.Simbolos.Union(afn_izquierdo.Simbolos)

            #unir transiciones del afn actual con el afn de los hijos
            afn.transiciones = afn.transiciones + afn_izquierdo.transiciones

            #estado final 
            afn.setEstadoFinal(afn_izquierdo.EstadosFinales.Elementos[-1])
                        
            return afn

        if nodo.simbolo == '*':

            #crear un afn
            afn = AFN()

            #agregar estado inicial del afn
            afn.estado_inicial = Estado(self.contador, 'normal')
            afn.agregar_estado(afn.estado_inicial)
            self.contador += 1

            #afn del hijo izquierdo
            afn_izquierdo = self.Thompson(nodo.hijo_izq)
            afn.agregar_transicion(afn.estado_inicial, afn_izquierdo.estado_inicial, 'ε')


            #agregar estado final
            estado_final = Estado(self.contador + 1, 'normal')
            afn.setEstadoFinal(estado_final)
            afn.agregar_estado(estado_final)
            self.contador += 1

            #agregar transiciones de los hijos
            afn.agregar_transicion(afn_izquierdo.EstadosFinales.Elementos[-1], estado_final, 'ε')
            afn.agregar_transicion(afn_izquierdo.EstadosFinales.Elementos[-1], afn_izquierdo.estado_inicial, 'ε')
            afn.agregar_transicion(afn.estado_inicial, estado_final, 'ε')

            #agregar simbolo del afn
            afn.agregar_simbolo('ε')

            #unir estados del afn actial con el afn de los hijos
            afn.Estados = afn.Estados.Union(afn_izquierdo.Estados)

            #unir simbolos del afn actual con el afn de los hijos
            afn.Simbolos = afn.Simbolos.Union(afn_izquierdo.Simbolos)

            #unir transiciones del afn actual con el afn de los hijos
            afn.transiciones = afn.transiciones + afn_izquierdo.transiciones

            #estado final
            afn.setEstadoFinal(afn_izquierdo.EstadosFinales.Elementos[-1])
           
            return afn


        if nodo.simbolo == '+':

            #crear un afn
            afn = AFN()

            #estado inicial
            afn.estado_inicial = Estado(self.contador, 'normal')
            afn.agregar_estado(afn.estado_inicial)

            #estado intermedio
            estado_intermedio = Estado(self.contador +1, 'normal')
            afn.agregar_estado(estado_intermedio)
            self.contador += 2

            #transicion entre estado inicial y estado intermedio
            afn.agregar_transicion(afn.estado_inicial, estado_intermedio, nodo.hijo_izq.simbolo)

            #agregar simbolo del afn
            afn.agregar_simbolo(nodo.hijo_izq.simbolo)

            #afn del hijo izquierdo
            afn_izquierdo = self.Thompson(nodo.hijo_izq)
            afn.agregar_transicion(estado_intermedio, afn_izquierdo.estado_inicial , 'ε')


            #agregar estado final
            estado_final = Estado(self.contador + 1, 'normal')
            afn.setEstadoFinal(estado_final)
            afn.agregar_estado(estado_final)
            self.contador += 1

            #agregar transiciones de los hijos
            afn.agregar_transicion(afn_izquierdo.EstadosFinales.Elementos[-1], estado_final, 'ε')
            afn.agregar_transicion(afn_izquierdo.EstadosFinales.Elementos[-1], afn_izquierdo.estado_inicial, 'ε')
            afn.agregar_transicion(estado_intermedio, estado_final, 'ε')

            #agregar simbolo del afn
            afn.agregar_simbolo('ε')

            #unir estados del afn actial con el afn de los hijos
            afn.Estados = afn.Estados.Union(afn_izquierdo.Estados)

            #unir simbolos del afn actual con el afn de los hijos
            afn.Simbolos = afn.Simbolos.Union(afn_izquierdo.Simbolos)

            #unir transiciones del afn actual con el afn de los hijos
            afn.transiciones = afn.transiciones + afn_izquierdo.transiciones

            return afn
         

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


    def graficar(self,afn, nombre_archivo):

        g = Digraph('AFN', filename=nombre_archivo)
        g.attr(rankdir='LR')

        # Agregar los estados al grafo
        for estado in afn.Estados.Elementos:
            if estado.tipo == 'inicial':
                g.node(str(estado.id), shape='circle')
                g.node ('', shape='none', height='0', width='0')
                g.edge('', str(estado.id))

            elif estado.tipo == 'final':
                g.node(str(estado.id), shape='doublecircle')
            else:
                g.node(str(estado.id), shape='circle')

        # Agregar las transiciones al grafo
        for transicion in afn.transiciones:
            g.edge(str(transicion[0].id), str(transicion[1].id), label=transicion[2])

        g.view()
