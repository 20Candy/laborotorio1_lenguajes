class Set:
    def __init__(self):
        self.elements = []

    def Intersection(self, A):
        intersection = Set()
        for elemento in self.elements:
            if elemento in A.elements:
                intersection.elements.append(elemento)
        return intersection

    def Union(self, A):
        union = Set()
        union.elements = self.elements + A.elements
        return union

    def Diference(self, A):
        diference = Set()
        for elemento in self.elements:
            if elemento not in A.elements:
                diference.elements.append(elemento)
        return diference

    def AddItem(self, elemento):
        self.elements.append(elemento)

    def Update(self, A):
        for elemento in A.elements:
            if elemento not in self.elements:
                self.elements.append(elemento)

    def Clear(self):
        self.elements = []

    def __str__(self):
        return str(self.elements)
        