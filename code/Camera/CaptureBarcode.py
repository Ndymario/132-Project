from picamera import PiCamera
from time import sleep

def takePicture():
    # make camera = PiCamera() to make it easier to code
    camera = PiCamera()

    # set camera resolution and framerate
    camera.resolution = (2592, 1944)
    camera.framerate = 15
    # show preview of camera
    camera.start_preview()

    # camera takes a picture if you hit ENTER
    button = raw_input("Press ENTER to take picture, b and ENTER to cancel. ")
    if (button == ""):
        # take a picture and save it to 132-project as barcode_01
        camera.capture("/home/pi/Documents/Python programs/132-project/132-Project/code/barcode_01.jpg")
        # turn on preview
        camera.stop_preview()
    elif (button == "b"):
        # turn off camera
        camera.stop_preview()
    camera.close()

#takePicture()
