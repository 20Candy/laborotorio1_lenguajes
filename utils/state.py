from utils.set import Set

class State:
    def __init__(self, id, type, AFN_states = None):
        self.id = id
        self.type = type
        self.AFN_states = AFN_states

    def __str__(self):
        return (str(self.id)+ " " + self.type)