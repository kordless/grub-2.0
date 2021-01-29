import cv2
import numpy as np

# Load image, grayscale, Otsu's threshold 
image = cv2.imread('images/1.png')
original = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours, obtain bounding box, extract and save ROI
ROI_number = 0
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

if len(cnts) < 2:
	# invert the image and try again to handle black backgrounds
	invert_flag = 1
	image = cv2.bitwise_not(image)
	original = image.copy()

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

	cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]
else:
	invert_flag = 0

for c in cnts:
    x,y,w,h = cv2.boundingRect(c)

    # only certain sized ranges
    if w < 97 and h < 97:
    	# smaller than a 100x100 square
    	continue

    if w < 7 or h < 7:
    	# one dimension smaller than 3
    	continue

    cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
    ROI = original[y:y+h, x:x+w]
    
    if invert_flag:
    	ROI = cv2.bitwise_not(ROI)

    cv2.imwrite('images/1/ROI_{}.png'.format(ROI_number), ROI)
    ROI_number += 1

image = cv2.imread('images/2.png')
image = cv2.bitwise_not(image)

original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours, obtain bounding box, extract and save ROI
ROI_number = 0
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

if len(cnts) < 2:
	# invert the image and try again to handle black backgrounds
	invert_flag = 1
	image = cv2.bitwise_not(image)
	original = image.copy()

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

	cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]
else:
	invert_flag = 0

for c in cnts:
    x,y,w,h = cv2.boundingRect(c)

    # only certain sized ranges
    if w < 97 and h < 97:
    	# smaller than a 100x100 square
    	continue

    if w < 7 or h < 7:
    	# one dimension smaller than 3
    	continue

    cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
    ROI = original[y:y+h, x:x+w]
    
    if invert_flag:
    	ROI = cv2.bitwise_not(ROI)

    cv2.imwrite('images/2/ROI_{}.png'.format(ROI_number), ROI)
    ROI_number += 1
