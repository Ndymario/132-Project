from pyzbar import pyzbar
import argparse
import cv2

# construct argument parser and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to input image")
args = vars(ap.parse_args())

# load image
image = cv2.imread(args["image"])

# find barcode and decode it
barcodes = pyzbar.decode(image)

for barcode in barcodes:
    # convert barcode data to a string to draw it
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type

    # draw the barcode data and type on image
    text = "{} ({})".format(barcodeData, barcodeType)

    # print the barcode type and data to the terminal
    print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))


