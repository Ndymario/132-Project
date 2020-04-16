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
    # draw box around barcode
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # convert barcode data to a string to draw it
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type

    # draw the barcode data and type on image
    text = "{} ({})".format(barcodeData, barcodeType)
    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # print the barcode type and data to the terminal
    print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

# show image
cv2.imshow("Image", image)
cv2.waitKey(0)
