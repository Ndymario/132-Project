from picamera import PiCamera
from setFocus import *
import RPi.GPIO as GPIO

# set up button
button = 18

# set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def takePicture():
    # make camera = PiCamera() to make it easier to code
    camera = PiCamera()

    # set camera focus
    setFocus()

    # set camera resolution and framerate
    camera.resolution = (2592, 1944)
    camera.framerate = 15
    # show preview of camera
    camera.start_preview()

    # camera takes a picture if you hit button on breadboard
    while (True):
        if (GPIO.input(button) == GPIO.HIGH):
            # take a picture and save it to 132-project as barcode_01
            camera.capture("/home/pi/Documents/Python programs/132-project/132-Project/code/barcode_01.jpg")
            # turn on preview
            camera.stop_preview()
            break
            
    camera.close()

#takePicture()
