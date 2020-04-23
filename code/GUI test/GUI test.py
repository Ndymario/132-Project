from Tkinter import *

WIDTH = 30
HEIGHT = 10


class MainGui(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

    def setupGUI(self):
        for i in range(len(alist)):
            if (alist[i] == "red"):
                BG = "red"
            else:
                BG = "green"
            TX = blist[i]
            text_frame = Label(self.master,text = "{}".format(TX), bg = "{}".format(BG),\
                               width = WIDTH, height = HEIGHT/8)

            text_frame.pack(side = TOP, fill = X)
            text_frame.pack_propagate(False)
        
        addbutton = Button(self.master, text =  "Add Item", fg = "black", width = (WIDTH)\
                           , height = (HEIGHT))
        addbutton.pack(side = LEFT)

        listbutton = Button(self.master, text =  "list", fg = "black", width = WIDTH\
                            ,height = (HEIGHT))
        listbutton.pack(side = LEFT)

        removebutton = Button(self.master, text =  "Remove Item", fg = "black",\
                              width = WIDTH,height = (HEIGHT))
        removebutton.pack(side = LEFT)

        
        






















############# Main #######################


window = Tk()

window.title("Kitchen")

p = MainGui(window)
p.setupGUI()

window.mainloop()
