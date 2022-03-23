import numpy as np
import math
import cv2

import extramath as em

class Joint:
	def __init__(self, label, degMin, degMax, index, end, base = 0):
		self.label = label
		self.degMin = degMin
		self.degMax = degMax
		self.index = index
		self.end = end
		self.base = base

	def getCurlAngle(self, lm):
		return em.angleByPoints(
			lm[self.index],
			lm[self.end],
			lm[self.base])

	def getCurlPercentage(self, lm):
		return self.angleToPercent(self.getCurlangle(lm))
	
	def angleToPercent(self, angle):
		p = em.map(angle, self.degMin, self.degMax, 100, 0)
		return np.clip(p, 0, 100)

fingers = [
Joint('Thumb', 120, 150, 1, 4),
Joint('Index', 50, 170, 5, 8),
Joint('Middle', 30, 170, 9, 12),
Joint('Ring', 30, 170, 13, 16),
Joint('Pinky', 60, 170, 17, 20),
]

def getJointDataString(landmarks):
	result = "### Joint Curl Data: ###\n"
	resultRaw = ""

	for joint in fingers:
		angle = np.rint(joint.getCurlAngle(landmarks))
		percentage = np.rint(joint.angleToPercent(angle))
		start = f"| {joint.label}:"

		result += start + f"{percentage}%".center(8) + '|'
		resultRaw += start + f"{angle}º".center(8) + '|'

	return result + '\n' + resultRaw
