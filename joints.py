import numpy as np
import math
import cv2

class Joint:
	def __init__(self, label, degMin, degMax, index, endOffset = 3, base = 0):
		self.label = label
		self.degMin = degMin
		self.degMax = degMax
		self.index = index
		self.end = index + endOffset
		self.base = base
	
	def getCurlPercentage(self, angle):
		p = map(angle, self.degMin, self.degMax, 100, 0)
		return np.rint(np.clip(p, 0, 100))

joints = [
# Finger data is represented with: label, minimum angle, maximum angle, and index of knuckle's control point
Joint('Thumb', 120, 150, 1),
Joint('Index', 50, 170, 5),
Joint('Middle', 30, 170, 9),
Joint('Ring', 30, 170, 13),
Joint('Pinky', 60, 170, 17),
]

def magnitude(v1, v2):
	return math.sqrt(
	(v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2 + (v1.z - v2.z) ** 2
	)

def getCurlAngle(landmarks, jointIndex):
	return getCurlAngleByJoint(landmarks, joints[jointIndex])

def getCurlPercentage(landmarks, jointIndex):
	joint = joints[jointIndex]
	angle = getCurlAngleByJoint(landmarks, joint)
	return joint.getCurlPercentage(angle)

def getCurlAngleByJoint(landmarks, joint):
	w = landmarks[joint.base]
	k = landmarks[joint.index]
	f = landmarks[joint.end]
	
	c = magnitude(f, k)
	b = magnitude(w, k)
	a = magnitude(f, w)
	
	return np.rad2deg(np.arccos((-a ** 2 + b ** 2 + c ** 2)/(2 * b * c)))

def getJointDataString(landmarks):

	result = "### Joint Curl Data: ###\n"
	resultRaw = ""

	for joint in joints:
		angle = getCurlAngleByJoint(landmarks, joint)
		percentage = joint.getCurlPercentage(angle)
		angle = np.rint(angle)
		start = f"| {finger.label}:"

		result += start + f"{percentage}%".center(8) + '|'
		resultRaw += start + f"{angle}º".center(8) + '|'

	return result + '\n' + resultRaw

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
