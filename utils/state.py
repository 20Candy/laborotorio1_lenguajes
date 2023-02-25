from utils.set import Set

class State:
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __str__(self):
        return (str(self.id)+ " " + self.type)