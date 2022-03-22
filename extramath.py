import numpy as np
import math

def magnitude(v1, v2):
	return math.sqrt(
	(v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2 + (v1.z - v2.z) ** 2
	)

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def angleByPoints(ptA, ptB, ptC):
	'''Calculates the angle at ptA on a triangle formed by ptA, ptB, and ptC'''	
	a = magnitude(ptB, ptC)
	b = magnitude(ptC, ptA)
	c = magnitude(ptB, ptA)
	
	return np.rad2deg(np.arccos((-a ** 2 + b ** 2 + c ** 2)/(2 * b * c)))
