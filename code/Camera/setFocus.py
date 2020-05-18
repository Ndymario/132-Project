import os

# sets focus of camera
def setFocus():
    # focus value of 532
    focus = 532
    value = (focus<<4) & 0x3ff0
    dat1 = (value>>8)&0x3f
    dat2 = value & 0xf0
    os.system("i2cset -y 0 0x0c %d %d" % (dat1,dat2))

#setFocus()
