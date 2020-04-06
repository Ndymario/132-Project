import requests
from bs4 import BeautifulSoup
from datetime import *



class Item(object):
    def __init__(self, name):
        self.name = name        
        self.today = date.today()

    

        
    def __str__(self):
        return "Name: {}".format(self.name)

class Perishable(Item):
    def __init__(self, name, experationDate):
        Item.__init__(self, name)
        self.experationDate = experationDate

    def __str__(self):
        return "Name: {} \nExperation: {}".format(self.name, self.experationDate)
        

        
class NonPerishable(Item):
    def __init__(self, name):
        Item.__init__(self, name)
###################### other def #########################

#   a function to look up a name
#   **** i dont know if this should be in a class because
#   **** all classes need a name before beang created       
def lookupname(barcode):
        url = 'https://www.barcodelookup.com/'
        barcode = barcode
        page = requests.get(url + barcode)
        soup = BeautifulSoup(page.content, 'lxml')
        item_name = soup.find('h4')
        bcheck = item_name.text.strip()
        
        if ("API" in bcheck):
            name = "Item not in DataBase!"
            

        else:
            name = namecheck(bcheck)
        return name
# a function to check to see if the barcode was corect
def namecheck(name):
    name = name
    check =raw_input( "Is this corect: {}? \nY/N  ".format(name))
    check = check.lower()
    if (check == "y" or check == "yes"):
        return name
    else:
        name = raw_input("Type corect name: ")
        return name

# a function to get the experation date
def getEXP():
    today = date.today()
    year = input("Year: ")
    # forces the year to be in corect format
    while (year < today.year):
        year = input("Year:(ex. 2020) ")    
    month = input("Month: ")
    while (month <1 or month > 12):
        month = input("Month:(ex. 5)")
    day = input("Day: ")
    # function is not finished days can still couse error with the month
    while (day < 0 or day > 31):
        day = input("Day: ")
    
    exp = date(year, month, day)
   
    return exp


######## some test code ########
# sample barcodes 054500193243 , 
barcode = raw_input(" enter a barcode ")
p1 = Perishable(lookupname(barcode),getEXP())


print p1 #sample to print out a parishable item
print "today is {}".format(p1.today) # was a sample to print todays date
remain = (p1.experationDate - p1.today) # sample to get how much longer till experation
print "{} has {} days left".format(p1.name, remain.days) # sample to get the remanig days
