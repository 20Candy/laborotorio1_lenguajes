class Simbolo:
    def __init__(self, c_id):
        self.id = self.toAscii(c_id)
        self.c_id = c_id

    def __str__(self):
        return str(self.id)
    
    def toAscii(self, c_id):
        if(c_id == "\\s"):
           return 32
        elif(c_id == "\\n"):
            return 10
        elif(c_id == "\\t"):
            return 9
        else:
            return ord(c_id)
