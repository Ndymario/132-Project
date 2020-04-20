from pyzbar import pyzbar
import cv2

# load image
image = cv2.imread("barcode_01.jpg")

# find barcode and decode it
barcodes = pyzbar.decode(image)

for barcode in barcodes:
    # convert barcode data to a string to draw it
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type

    # print the barcode type and data to the terminal
    print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
