import numpy as np
import math
import os
import cv2

class Finger:
	def __init__(self, label, degMin, degMax, index):
		self.label = label
		self.degMin = degMin
		self.degMax = degMax
		self.index = index
		self.end = self.index + 3
	
	def getCurlPercentage(self, angle):
		p = map(angle, self.degMin, self.degMax, 0, 100)
		return np.rint(np.clip(p, 0, 100))

fingers = [
# Finger data is represented with: label, minimum angle, maximum angle, and index of knuckle's control point
Finger('Thumb', 120, 150, 1),
Finger('Index', 50, 170, 5),
Finger('Middle', 30, 170, 9),
Finger('Ring', 30, 170, 13),
Finger('Pinky', 60, 170, 17),
]

# Stuff for putting data on the camera output
lineHeight = 50
textColor = (0, 255, 255)
font = cv2.FONT_HERSHEY_PLAIN
textSize = 0.5

def magnitude(v1, v2):
	return math.sqrt(
	(v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2 + (v1.z - v2.z) ** 2
	)

def getCurlAngle(landmarks, fingerIndex):
	return getCurlAngleByFinger(landmarks, fingers[fingerIndex])

def getCurlPercentage(landmarks, fingerIndex):
	finger = fingers[fingerIndex]
	angle = np.rad2deg(getCurlAngleByFinger(landmarks, finger))
	return finger.getCurlPercentage(angle)

def getCurlAngleByFinger(landmarks, finger):
	w = landmarks[0]
	k = landmarks[finger.index]
	f = landmarks[finger.end]
	
	c = magnitude(f, k)
	b = magnitude(w, k)
	a = magnitude(f, w)
	
	return np.arccos((-a ** 2 + b ** 2 + c ** 2)/(2 * b * c))

def getFingerDataString(landmarks):

	result = "### Finger Curl Data: ###\n"
	resultRaw = ""

	for finger in fingers:
		angle = np.rad2deg(getCurlAngleByFinger(landmarks, finger))
		percentage = finger.getCurlPercentage(angle)
		angle = np.rint(angle)
		start = f"| {finger.label}:"

		result += start + f"{percentage}%".center(8) + '|'
		resultRaw += start + f"{angle}º".center(8) + '|'
	os.system('clear')

	return result + '\n' + resultRaw

def putFingerData(landmarks, image):
	
	sizeX = image.shape[1]
	sizeY = image.shape[0]

	image = cv2.flip(image, 1)

	for finger in fingers:
		angle = np.rad2deg(getCurlAngleByFinger(landmarks, finger))
		percentage = finger.getCurlPercentage(angle)
		angle = np.rint(angle)

		fingerEndPos = landmarks[finger.end]
		x = np.rint(sizeX * (1 - fingerEndPos.x))
		y = np.rint(sizeY * fingerEndPos.y)
		cv2.putText(image, f"{percentage}% | {angle}d", (50, 50), font, textSize, textColor)
	
	return cv2.flip(image, 1)

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
