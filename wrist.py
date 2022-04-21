import extramath as em

from joints import Joint

class Wrist(Joint):
	def __init__(self, label, degMin, degMax, index, end, base, indexIsFromPose):
		super().__init__(label, degMin, degMax, index, end, base)
		self.indexIsFromPose = indexIsFromPose
	
	def getCurlAngle(self, poselm, handlm):
		return em.angleByPoints(
			(poselm if self.indexIsFromPose else handlm)[self.index],
			handlm[self.end],
			poselm[self.base])

	def getCurlPercentage(self, poselm, handlm):
		return super().angleToPercent(self.getCurlAngle(poselm, handlm))

wrist = Wrist("R Wrist", 50, 150, 0, 9, 14, False)
