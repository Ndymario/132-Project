class Item(object):
    def __init__(self, name):
        self.name = name
        self.exporationDate = None

class Perishable(Item):
    def __init__(self, name):
        Item.__init__(self, name)
        self.exporationDate = True

class NonPerishable(Item):
    def __init__(self, name):
        Item.__init__(self, name)
        self.exporationDate = False
        
