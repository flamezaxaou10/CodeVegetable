# USAGE
# python detect_color.py --image pokemon_games.png

# import the necessary packages
import numpy as np
import argparse
import cv2
import imutils

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])

height, width, channels = image.shape
gridY = int(height/3)
gridX = int(width/4)
# define the list of boundaries
boundaries = [
	([146, 95, 46], [195, 100, 50]),
	([135, 40, 40], [156, 60, 50])
]

hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
# loop over the boundaries
for (lower, upper) in boundaries:
	# create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")
	lower = np.array([15,65,65])
	upper = np.array([255,255,255])
	# find the colors within the specified boundaries and apply
	# the mask
	mask = cv2.inRange(hsv, lower, upper)
	output = cv2.bitwise_and(image, image, mask = mask)

	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
	cnts = cnts[:12]

	for idx, c in enumerate(cnts) :
		rec = cv2.boundingRect(c)
		area = cv2.contourArea(c)
		if (area>100):
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.01 * peri, True)
			#if len(approx) >= 4:
			screenCnt = approx
			centerX = int((screenCnt[0][0][0] + screenCnt[int(len(screenCnt)/2)][0][0])/2)
			centerY = int((screenCnt[int(len(screenCnt)/4)][0][1] + screenCnt[int(len(screenCnt)/4*3)][0][1])/2)
			centerCo = (centerX , centerY)
			col = int(centerX/gridX)
			row = int(centerY/gridY)
			hole = row*4+col+1
			cv2.drawContours(image, [screenCnt], -1, (255, 255, 0), 2)
			cv2.putText(image, "{}".format(str(hole)) + ": {}".format(str(area)), centerCo,
        	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
	# time.sleep(5)
	# show the images
	cv2.imshow("images", np.hstack([image, output]))
	cv2.waitKey(0)
	cv2.destroyAllWindows()