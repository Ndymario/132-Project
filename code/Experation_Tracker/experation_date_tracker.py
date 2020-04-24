#######################################
# Contributors (to this file): Nolan Yelverton
# Date: 04/01/20
# Description: Settup for how we're going to store our experation dates
#######################################

# Import datetime so we can get the current time.
from datetime import datetime

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

    # Returns the item that is most about to expire, if it exists
    def __str__(self):
        oldestItem = 0

        try:
            return "Item: {}\nExp: {}".format(self.itemList[oldestItem], self.experationDict[self.itemList[oldestItem]])
        except IndexError:
            return "There are no foods in the list!"
    
    # Function that can add items & experation dates to our dict.
    # Also stores items into a list of items
    def itemAdder(self, item, date):
        self.experationDict[item] = date
        self.itemList.append(item)

    # Function that will remove items when they are expired.
    def itemRemover(self):
        # Get today's date
        today = datetime.today().strftime('%m/%d/%y')

        # Split the date into Month/Day/Year
        date = today.split("/")

        # Get the oldest food experation date, if it exists
        try:
            oldestItem = self.itemList[0]
        except:
            print("There aren't any foods in the list!")

        # Get the date of the oldest item
        experation = self.experationDict[oldestItem]

        expDate = experation.split("/")

        # If the year of the food's experation date is older than the current date, remove it
        if (expDate[2] < date[2]):
            self.itemList.remove(oldestItem)

        # If the month of the food's experation date is older than the current date, remove it
        elif (expDate[0] < date[0]):
            self.itemList.remove(oldestItem)

        # If the day of the food's experation date is older than the current date, remove it
        elif (expDate[1] < date[1]):
            self.itemList.remove(oldestItem)

        # If the food's experation date is todays date, say that the food expires today
        elif (expDate[0] == date[0] and expDate[1] == date[1]):
            print("Your {} expires today!".format(oldestItem))

        # Otherwise, just say nothing has expired
        else:
            print("Nothing has expired!")
    
#######################################

# Sample of taking an input and handeling experation dates
et = ExperationTracker()

food = raw_input("Please enter the food's name: ")

date = raw_input("Please enter the food's expiration date (MM/DD/YY): ")

et.itemAdder(food, date)
print(et)
print
et.itemRemover()
print
print(et)
