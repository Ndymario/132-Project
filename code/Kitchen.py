#######################################
# Contributors (to this file):
# Date: 04/20/20
# Description: The main program.
#######################################

# Import libraries we want to use
import sys
import requests
from bs4 import BeautifulSoup
from datetime import *
import pickle

# Allow us to import a .py from another folder; makes the backend cleaner
sys.path.insert(1, "./Camera")
sys.path.insert(1, "./Experation_Tracker")

# Import helper python files
from barcodeScanner3function import *
from experation_date_tracker import *

DEBUG = True
SAVEFILE = "Rick"

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
        self.time_left = 100

    @property
    def time_left(self):
        return self._time_left

    @time_left.setter
    def time_left(self,val):
        remain = (self.experationDate - self.today)
        self._time_left = remain.days

    def updateEXP(self):
        self.today = date.today()
        remain = (self.experationDate - self.today)
        self.time_left = remain.days
    
    def __str__(self):
        return "Name: {} \nExperation: {} \nDaysleft: {}".format(self.name, self.experationDate, self.time_left)
        

        
class NonPerishable(Item):
    def __init__(self, name):
        Item.__init__(self, name)
###################### other def #########################

#   a function to look up a name
#   **** i dont know if this should be in a class because
#   **** all classes need a name before beang created
def lookupname(barcode):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac'\
               'OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url = 'https://www.barcodelookup.com/'
    barcode = barcode
    if (DEBUG):
        print "(lookupname) barcode = {}".format(barcode)
    page = requests.get(url + barcode, headers = headers)
    if (DEBUG):
        print "(lookupname) page = {}".format(page)
    soup = BeautifulSoup(page.content, 'lxml')
    item_name = soup.find('h4')
    if (DEBUG):
        print "(lookupname) item_name = {}".format(item_name)
    bcheck = item_name.text.strip()
    name = namecheck(bcheck)
    return name
# a function to check to see if the barcode was corect
def namecheck(tempname):
    name = tempname
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
# a function to save data when python is off use name "mydata" for now
def savedata(val, name):
    with open('{}.pickle'.format(name), 'wb') as mysavedata:
        pickle.dump(val, mysavedata)
# a function to load data after python is off use name "mydata" for now can change it if there are more things to save
def loaddata(name):
    with open('{}.pickle'.format(name), 'rb') as myrestoredata:
        alist = pickle.load(myrestoredata)
        return alist

# adds an item to the list
def additem(alist):
    barcode = encodeBarcode()
    if (DEBUG):
        print "(additem)barcode = {}".format(barcode)
    name = lookupname(barcode)
    experation = getEXP()
    item = Perishable(name, experation)
    alist.append(item)
    return alist

def sortitems(alist):
    n = len(alist)
    for i in range(0, n-1):
        minpos = i
        for j in range(i + 1, n):
            if(alist[j].time_left < alist[minpos].time_left):
                minpos = j
        temp = alist[i]
        alist[i] = alist[minpos]
        alist[minpos] = temp
        
    return alist
def update():
    alist = loaddata(SAVEFILE)
    for i in range(len(alist)):
        alist[i].updateEXP()
    return alist
    
######## some test code ########
# sample barcodes 054500193243 ,
alist = []
print "The curent list is as follows"

alist = update()
for i in range(len(alist)):
    print alist[i]


##alist = additem(alist)
alist = sortitems(alist)


print " \nThe list after addind a new item"
for i in range(len(alist)):
    print alist[i]


savedata(alist, SAVEFILE)


### old code used to run test
##print "#"*30
##name = "test item"
##experation = getEXP()
##p1 = Perishable(name, experation)
##print p1 #sample to print out a parishable item
##print "today is {}".format(p1.today) # was a sample to print todays date
##remain = (p1.experationDate - p1.today) # sample to get how much longer till experation
##print "{} has {} days left".format(p1.name, remain.days) # sample to get the remanig days
##print p1.time_left
##p1.updateEXP()
##print p1.time_left
