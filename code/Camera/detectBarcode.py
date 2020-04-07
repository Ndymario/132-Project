import numpy as np
import argparse
import imutils
import cv2

# construct the argument
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to the file")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
# convert to greyscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# compute the Scharr gradient magnitude for the image
# in the x and y direction
ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
gradX = cv2.Sobel(gray, ddepth = ddepth, dx = 1, dy = 0, ksize = -1)
gradY = cv2.Sobel(gray, ddepth = ddepth, dx = 0, dy = 1, ksize = -1)

# subtract grady from gradX
gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)

# blur the image
blurred = cv2.blur(gradient, (9,9))
# threshold the image
(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)


# close gaps between vertical bars
# construct a closing kernal and apply it to the threshold image
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernal)

# image could potientially have small blobs that might interfier
# this will clean it up by performing a series of erosions and
# dilations
closed = cv2.erode(closed, None, iterations = 4)
closed = cv2.dilate(closed, None, iterations = 4)

# find and sort the contours by their area in the image 
# keeping the largest one
cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

# compute the rotated bounding bos of the largest contour
rect = cv2.minAreaRect(c)
box = cv2.cv.BowPionts(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
box = np.int0(box)

# draw a box around the barcode and display the image
cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
cv2.imshow("Image", image)
cv2.waitKey(0)
