class Set:
    def __init__(self):
        self.Elementos = []

    def Interseccion(self, A):
        interseccion = Set()
        for elemento in self.Elementos:
            if elemento in A.Elementos:
                interseccion.Elementos.append(elemento)
        return interseccion

    def Union(self, A):
        union = Set()
        union.Elementos = self.Elementos + A.Elementos
        return union

    def Diferencia(self, A):
        diferencia = Set()
        for elemento in self.Elementos:
            if elemento not in A.Elementos:
                diferencia.Elementos.append(elemento)
        return diferencia

    def AddItem(self, elemento):
        self.Elementos.append(elemento)