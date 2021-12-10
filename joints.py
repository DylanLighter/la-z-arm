import numpy as np
import math
import cv2

class Joint:
	def __init__(self, label, degMin, degMax, index, end, base = 0):
		self.label = label
		self.degMin = degMin
		self.degMax = degMax
		self.index = index
		self.end = end
		self.base = base

	def getCurlAngle(self, landmarks):
		w = landmarks[self.base]
		k = landmarks[self.index]
		f = landmarks[self.end]
		
		c = magnitude(f, k)
		b = magnitude(w, k)
		a = magnitude(f, w)
		
		return np.rad2deg(np.arccos((-a ** 2 + b ** 2 + c ** 2)/(2 * b * c)))
	
	def getCurlPercentage(self, landmarks):
		p = map(self.getCurlAngle(landmarks), self.degMin, self.degMax, 100, 0)
		return np.rint(np.clip(p, 0, 100))

joints = [
Joint('Thumb', 120, 150, 1, 4),
Joint('Index', 50, 170, 5, 8),
Joint('Middle', 30, 170, 9, 12),
Joint('Ring', 30, 170, 13, 16),
Joint('Pinky', 60, 170, 17, 20),
]

def magnitude(v1, v2):
	return math.sqrt(
	(v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2 + (v1.z - v2.z) ** 2
	)

def getCurlAngle(landmarks, jointIndex):
	return getCurlAngleByJoint(landmarks, joints[jointIndex])

def getCurlPercentage(landmarks, jointIndex):
	joint = joints[jointIndex]
	return joint.getCurlPercentage(landmarks)

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
		percentage = joint.getCurlPercentage(landmarks)
		angle = np.rint(joint.getCurlAngle(landmarks))
		start = f"| {joint.label}:"

		result += start + f"{percentage}%".center(8) + '|'
		resultRaw += start + f"{angle}º".center(8) + '|'

	return result + '\n' + resultRaw

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
