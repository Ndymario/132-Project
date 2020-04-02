#######################################
# Contributors (to this file): Nolan Yelverton
# Date: 04/01/20
# Description: Settup for how we're going to store our experation dates
#######################################

class ExperationTracker(object):
    # Set up a dictionary to store our item's experation dates
    experationDict = {}

    # Set up a list to store our items
    itemList =  []

    def __init__(self):
        pass

    # --Begin Accessors & Mutators--
    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date
    # --End Accessors & Mutators--

    # Returns the most
    def __str__(self):
        return "Item: {}\nExp: {}".format(self.itemList[i], self.experationDict["Apple"])
    
    # Function that can add items & experation dates to our dict.
    # Also stores items into a list of items
    def itemAdder(self, item, date):
        self.experationDict[item] = date
        self.itemList.append(item)

    # Function that will remove items when they are expired.
    def itemRemover(self, item, date):
        pass
    
#######################################
et = ExperationTracker()
et.itemAdder("Apple", "04/01/20")
et.itemAdder("Orange","04/02/20")
print(et)
