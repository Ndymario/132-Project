class Item(object):
    def __init__(self, name):
        self.name = name

class Perishable(Item):
    def __init__(self, name, experationDate):
        Item.__init__(self, name)
        self.experationDate = experationDate

class NonPerishable(Item):
    def __init__(self, name):
        Item.__init__(self, name)
        