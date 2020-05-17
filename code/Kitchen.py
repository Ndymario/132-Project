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
import Tkinter as tk
# Allow us to import a .py from another folder; makes the backend cleaner
sys.path.insert(1, "./Camera")
sys.path.insert(1, "./Experation_Tracker")

# Import helper python files
from barcodeScanner3function import *
#from experation_date_tracker import *
# global variables
DEBUG = False
CLEAR_LIST = True # Make true if you want the list clear each time the program is run
                  # make False if you want to bring back the last items enterd
SAVEFILE = "Rick"
alist = []
WIDTH = 30
HEIGHT = 10
STYLE = "Arial"
LARGE_FONT = (STYLE, 12)

# Variables for buttons on home screen
BUTTON_FONT = (STYLE, 17)
BUTTON_HEIGHT = 5
BUTTON_WIDTH = 15

TODAY = date.today()
NAME_CHECK = ""
MONTH_CHECK = "{}".format(TODAY.month)
DAY_CHECK = "{}".format(TODAY.day)
YEAR_CHECK = "{}".format(TODAY.year)
MANUAL_CHECK = 0 # a variable that lets certan buttons show up under right conditions


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
# top level of GUI builds a frame containg all other frames
class GUI(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # creates the GUE "manual add each page to the list
        for F in [MainGui, ADD, Manual, SCAN, List, Remove]:

            frame = F(container,self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainGui)
      
    def show_frame(self, cont):
        
        frame = self.frames[cont]        
        frame.tkraise()
        
        
# Main page of GUI has the list of item and buttons to add items                
class MainGui(tk.Frame):
    
    def __init__(self, parent, controller):
        global NAME_CHECK, MONTH_CHECK, DAY_CHECK, YEAR_CHECK, TODAY
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Kitchen Gadget", font = LARGE_FONT)
        label.pack(pady=10,padx=10)
        # if statment to clear the list using a global variable
        if (not CLEAR_LIST):
            global alist
            alist = updateList()
            alist = sortitems(alist)
            
        else:
            global CLEAR_LIST
            alist = []
            CLEAR_LIST = False
        if (DEBUG):
            print "(MainGui) clear_list -> {}".format(CLEAR_LIST)
        if (len(alist) <= 5):
            for i in range(len(alist)):
                if (alist[i].time_left <= 3):
                    BG = "red"
                elif (alist[i].time_left <= 7):
                    BG = "yellow"
                else:
                    BG = "green"
                TX = "{}  EXPERATION: {}".format(alist[i].name,alist[i].experationDate)
                text_frame = tk.Label(self,text = "{}".format(TX), bg = "{}".format(BG),\
                                   width = WIDTH, height = HEIGHT/8)

                text_frame.pack(side = "top", fill = "x")
                text_frame.pack_propagate(False)
        else:
            for i in range(5):
                if (alist[i].time_left <= 3):
                    BG = "red"
                elif (alist[i].time_left <= 7):
                    BG = "yellow"
                else:
                    BG = "green"
                TX = "{}  EXPERATION: {}".format(alist[i].name,alist[i].experationDate)
                text_frame = tk.Label(self,text = "{}".format(TX), bg = "{}".format(BG),\
                                   width = WIDTH, height = HEIGHT/8)

                text_frame.pack(side = "top", fill = "x")
                text_frame.pack_propagate(False)
                
        NAME_CHECK = ""
        MONTH_CHECK = "{}".format(TODAY.month)
        DAY_CHECK = "{}".format(TODAY.day)
        YEAR_CHECK = "{}".format(TODAY.year)
        addbutton = tk.Button(self, text =  "Add Item", fg = "black", width = (BUTTON_WIDTH)\
                           , height = (BUTTON_HEIGHT), font = BUTTON_FONT, command=lambda: controller.show_frame(ADD))
        addbutton.pack(side = "left")

        listbutton = tk.Button(self, text =  "List", fg = "black", width = BUTTON_WIDTH\
                            ,height = (BUTTON_HEIGHT), font = BUTTON_FONT, command=lambda: controller.show_frame(List))
        listbutton.pack(side = "left")

        removebutton = tk.Button(self, text =  "Remove Item", fg = "black",\
                              width = BUTTON_WIDTH, height = (BUTTON_HEIGHT), font = BUTTON_FONT, command=lambda: controller.show_frame(Remove))
        removebutton.pack(side = "left")
# GUI for when add button is pressed
class ADD(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="How would you like to enter the item?", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        def milk():
            global NAME_CHECK, MONTH_CHECK, DAY_CHECK, YEAR_CHECK, TODAY
            if (DAY_CHECK <= "18"):
                DAY_CHECK = "{}".format((TODAY.day + 10))
            else:
                MONTH_CHECK = "{}".format(TODAY.month + 1)
                DAY_CHECK = "{}".format(((TODAY.day + 10) - 28))
                if (MONTH_CHECK =="13"):
                    MONTH_CHECK = "1"
                if DAY_CHECK == "0":
                    DAY_CHECK = "1"
            NAME_CHECK = "Milk"        

            frame = Manual(parent,controller)

            controller.frames[Manual] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update

        def bread():
            global NAME_CHECK, MONTH_CHECK, DAY_CHECK, YEAR_CHECK, TODAY
            if (DAY_CHECK <= "18"):
                DAY_CHECK = "{}".format((TODAY.day + 10))
            else:
                MONTH_CHECK = "{}".format(TODAY.month + 1)
                DAY_CHECK = "{}".format(((TODAY.day + 10) - 28))
                if (MONTH_CHECK =="13"):
                    MONTH_CHECK = "1"
                if DAY_CHECK == "0":
                    DAY_CHECK = "1"
            NAME_CHECK = "Bread"        

            frame = Manual(parent,controller)

            controller.frames[Manual] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update

        def leftover():
            global NAME_CHECK, MONTH_CHECK, DAY_CHECK, YEAR_CHECK, TODAY
            if (DAY_CHECK <= "21"):
                DAY_CHECK = "{}".format((TODAY.day + 7))
            else:
                MONTH_CHECK = "{}".format(TODAY.month + 1)
                DAY_CHECK = "{}".format(((TODAY.day + 7) - 28))
                if (MONTH_CHECK =="13"):
                    MONTH_CHECK = "1"
                if DAY_CHECK == "0":
                    DAY_CHECK = "1"
            NAME_CHECK = "Leftovers"       

            frame = Manual(parent,controller)

            controller.frames[Manual] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update

        def cancel():
            frame = MainGui(parent,controller)

            controller.frames[MainGui] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update
            
            

        button1 = tk.Button(self, text="Scan",
                            command=lambda: controller.show_frame(SCAN))
        button1.pack()

        button2 = tk.Button(self, text="Manual",
                            command=lambda: controller.show_frame(Manual))
        button2.pack()
        
        button3 = tk.Button(self, text="Milk",
                            command= milk)
        button3.pack()
        
        button4 = tk.Button(self, text="Bread",
                            command= bread)
        button4.pack()

        button5 = tk.Button(self, text="Leftovers",
                            command= leftover)
        button5.pack()
        
        cancel = tk.Button(self, text="Cancel",
                            command= cancel)
        cancel.pack()
#GUI for when add->Manual is pressed
class Manual(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Manualy enter item", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        name = 1
        month =1
        day = 1
        year =1
        global alist, NAME_CHECK, MONTH_CHECK, DAY_CHECK, YEAR_CHECK, MANUAL_CHECK
        # function that is called when enter button is pushed
        def callback():
            global alist, NAME_CHECK, MONTH_CHECK, DAY_CHECK, YEAR_CHECK, MANUAL_CHECK
            NAME_CHECK = e1.get()
            month = int(e2.get())
            day = int(e3.get())
            year = int(e4.get())
            if (month <= 12 and day <= 31 and year >= 2020):                
                MONTH_CHECK = month                       
                DAY_CHECK = day
                YEAR_CHECK = year
                MANUAL_CHECK = 1
            # needed to reset the frame ********************************
            frame = Manual(parent,controller)

            controller.frames[Manual] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update
            #**************************************************************
            # calls function to show a specific frame
            controller.show_frame(Manual)
        # function called when submit button is pushed
        def callbacksubmit():
            global alist, NAME_CHECK, MONTH_CHECK, DAY_CHECK, YEAR_CHECK, MANUAL_CHECK
            exp = date(YEAR_CHECK, MONTH_CHECK, DAY_CHECK)
            alist = additemManual(alist, NAME_CHECK, exp)
            savedata(alist, SAVEFILE)
            MANUAL_CHECK = 0
            frame = Manual(parent,controller)

            controller.frames[Manual] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update
            frame = MainGui(parent,controller)

            controller.frames[MainGui] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update
            
            controller.show_frame(MainGui)
        def cancel():
            frame = MainGui(parent,controller)

            controller.frames[MainGui] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update
        l1 = tk.Label(self, text= "Name: ")
        l1.pack()
        
        e1 = tk.Entry(self, bg ="white")
        e1.insert(0, "{}".format(NAME_CHECK))
        e1.pack()
        
        l2 = tk.Label(self, text= "Month: ")
        l2.pack()
        e2 = tk.Entry(self, bg ="white")
        e2.insert(0, "{}".format(MONTH_CHECK))
        e2.pack()

        l3 = tk.Label(self, text= "Day: ")
        l3.pack()
        e3 = tk.Entry(self, bg ="white")
        e3.insert(0, "{}".format(DAY_CHECK))
        e3.pack()

        l4 = tk.Label(self, text= "Year: ")
        l4.pack()
        e4 = tk.Entry(self, bg ="white")
        e4.insert(0, "{}".format(YEAR_CHECK))
        e4.pack()

        button1 = tk.Button(self, text="ENTER",
                            command = callback)
        button1.pack()

        cancel = tk.Button(self, text="Cancel",
                            command= cancel)
        cancel.pack()
        
        if (MANUAL_CHECK == 1):
            submitbutton = tk.Button(self, text="submit",
                            command = callbacksubmit)
            submitbutton.pack()
# GUI for when ADD->SCAN is pressed
class SCAN(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="SCAN AN item", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        name = 1
        month =1
        day = 1
        year =1
        global alist, NAME_CHECK, MONTH_CHECK, DAY_CHECK, YEAR_CHECK, MANUAL_CHECK
        # when scan is pressed calls the scan fuction then checks to se if a valid barcode is there
        def callbackscan():
            global alist, NAME_CHECK, MONTH_CHECK, DAY_CHECK, YEAR_CHECK, MANUAL_CHECK
            barcode = encodeBarcode()    
            count = 0
            if (DEBUG):
                print "(scan)barcode = {}".format(barcode)
            if (barcode == None):        
                count = 1
                barcode = encodeBarcode()
            if (count == 1 and barcode == None):
                name = "cant get name enter manual"
            else:       
                name = lookupname(barcode)
                NAME_CHECK = name
                DAY_CHECK = ""
                MONTH_CHECK = ""
            frame = SCAN(parent,controller)

            controller.frames[SCAN] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update
            
            controller.show_frame(SCAN)
        # after all entery windows are filled out this funchion checks to make shure all good
        def callback():
            global alist, NAME_CHECK, MONTH_CHECK, DAY_CHECK, YEAR_CHECK, MANUAL_CHECK
            
            NAME_CHECK = e1.get()
            month = int(e2.get())
            day = int(e3.get())
            year = int(e4.get())
            if (month <= 12 and day <= 31 and year >= 2020):                
                MONTH_CHECK = month                       
                DAY_CHECK = day
                YEAR_CHECK = year
                MANUAL_CHECK = 1
            frame = SCAN(parent,controller)

            controller.frames[SCAN] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update
            
            controller.show_frame(SCAN)
        # creates the items and saves them to external file
        def callbacksubmit():
            global alist, NAME_CHECK, MONTH_CHECK, DAY_CHECK, YEAR_CHECK, MANUAL_CHECK
            exp = date(YEAR_CHECK, MONTH_CHECK, DAY_CHECK)
            alist = additemManual(alist, NAME_CHECK, exp)
            savedata(alist, SAVEFILE)
            MANUAL_CHECK = 0
            frame = SCAN(parent,controller)

            controller.frames[SCAN] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update
            frame = MainGui(parent,controller)

            controller.frames[MainGui] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update
            
            controller.show_frame(MainGui)
        if (MANUAL_CHECK == 0):
            namecheck = "press scan if incoretct enter name"
        else:
            namecheck = "name"
        def cancel():
            frame = MainGui(parent,controller)

            controller.frames[MainGui] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update
        l1 = tk.Label(self, text= "{}".format(namecheck))
        l1.pack()
        
        e1 = tk.Entry(self, bg ="white")
        e1.insert(0, "{}".format(NAME_CHECK))
        e1.pack()
        
        l2 = tk.Label(self, text= "Month: ")
        l2.pack()
        e2 = tk.Entry(self, bg ="white")
        e2.insert(0, "{}".format(MONTH_CHECK))
        e2.pack()

        l3 = tk.Label(self, text= "Day: ")
        l3.pack()
        e3 = tk.Entry(self, bg ="white")
        e3.insert(0, "{}".format(DAY_CHECK))
        e3.pack()

        l4 = tk.Label(self, text= "Year: ")
        l4.pack()
        e4 = tk.Entry(self, bg ="white")
        e4.insert(0, "{}".format(YEAR_CHECK))
        e4.pack()

        button1 = tk.Button(self, text="ENTER",
                            command = callback)
        button1.pack()
        scan = tk.Button(self, text="scan",
                            command = callbackscan)
        scan.pack()

        cancel = tk.Button(self, text="Cancel",
                            command= cancel)
        cancel.pack()
        
        if (MANUAL_CHECK == 1):
            submitbutton = tk.Button(self, text="submit",
                            command = callbacksubmit)
            submitbutton.pack()            
            
# Add GUI for viewing the entire list
class List(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Here are all of the foods stored inside of the list:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        def cancel():
            frame = MainGui(parent,controller)

            controller.frames[MainGui] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update
        
        cancel = tk.Button(self, text="Back",
                            command= cancel)
        cancel.pack()

# Add GUI for removing from the list
class Remove(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="What would you like to remove?", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        def cancel():
            frame = MainGui(parent,controller)

            controller.frames[MainGui] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            controller.frames.update
        
        cancel = tk.Button(self, text="Back",
                            command= cancel)
        cancel.pack()
        
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
    name = bcheck
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
def additem(alist,exp):
    barcode = encodeBarcode()    
    count = 0
    if (DEBUG):
        print "(additem)barcode = {}".format(barcode)
    if (barcode == None):        
        count = 1
        barcode = encodeBarcode()
    if (count == 1 and barcode == None):
        name = raw_input("enter name")
    else:       
        name = lookupname(barcode)
    experation = exp
    item = Perishable(name, experation)
    alist.append(item)
    return name
# manualy adds item !! what is used whith the GUI !!
def additemManual(alist, name, experation):
    item = Perishable(name, experation)
    alist.append(item)
    return alist
# function to sort the list    
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
# a function to load the saved files to a list
def updateList():
    alist = loaddata(SAVEFILE)
    for i in range(len(alist)):
        alist[i].updateEXP()
    return alist
    
######## MAIN CODE ########




if (DEBUG):
    alist = updateList()  
    alist = sortitems(alist)
    print "The curent list at startup is as follows"
    for i in range(len(alist)):
        print alist[i]










window = tk
window = GUI()

window.title("Kitchen")



window.mainloop()
if (DEBUG):
    print " \nThe list after closing GUI"
    for i in range(len(alist)):
        print alist[i]

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
