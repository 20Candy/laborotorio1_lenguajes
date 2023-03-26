class Simbolo:
    def __init__(self, c_id):
        self.id = ord(c_id)
        self.c_id = c_id

    def __str__(self):
        return str(self.id)
