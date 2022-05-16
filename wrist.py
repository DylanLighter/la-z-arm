import extramath as em
import numpy as np
from scipy.spatial.transform import Rotation as R

from joints import Joint

class Wrist(Joint):
	# Axis reference is used to rotate wrist vector along side of palm
	# Should be assigned to the most immobile knuckle
	def __init__(self, label, degMin, degMax, index, end, base, axisReference):
		super().__init__(label, degMin, degMax, index, end, base)
		self.axisRef = axisReference
	
	def getCurlAngle(self, poselm, handlm):
		base = poselm[self.base]
		end = handlm[self.end]
		index = handlm[self.index]
		ref = handlm[self.axisRef]
		v1 = normVec(base, index)
		rot = rotFromAxis(normVec(ref, index), 90)
		v2 = rot.apply(normVec(end, index))
		return np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0)) * 90

	def getCurlPercentage(self, poselm, handlm):
		return super().angleToPercent(self.getCurlAngle(poselm, handlm))

wrist = Wrist("R Wrist", 0, 180, 0, 9, 14, 5)

def vec(p):
	return np.array([p.x, p.y, p.z])

def normVec(p1, p2):
	v = vec(p1) - vec(p2)
	return v / np.linalg.norm(v)

def rotFromAxis(axis, deg):
	vec = deg * axis
	return R.from_rotvec(vec)
