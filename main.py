import cv2
import os

from joints import *
from motors import *
from hands import *
from pose import *

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # cls for Windows (for testing off rig)
        command = 'cls'
    os.system(command)

cap = cv2.VideoCapture(0)

# Set to True to disable motor movement
reportOnly = False

while cap.isOpened():
	success, image = cap.read()
	if not success:
		print("Ignoring empty camera frame.")
		# If loading a video, use 'break' instead of 'continue'.
		continue
	
	image.flags.writeable = False
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	
	hand_landmarks = processHand(image)
	pose_landmarks = processPose(image)

	clearConsole()
	
	if reportOnly:
		if hand_landmarks:
			print(getJointDataString(hand_landmarks.landmark))
	else:
		if hand_landmarks:
			landmark = hand_landmarks.landmark
			for i in range(5):
				rotateJoint(i, getCurlPercentage(landmark, i))
		else:
			print('No hand detected.')

		if pose_landmarks:
			rotateJoint(5, getCurlPercentage(pose_landmarks.landmark, 5))

	image.flags.writeable = True
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

	drawHandLandmarks(image, hand_landmarks)
	drawPoseLandmarks(image, pose_landmarks)

	# Flip the image horizontally for a selfie-view display.
	image = cv2.flip(image, 1)

	cv2.imshow('MediaPipe Hands', image)

	if cv2.waitKey(5) & 0xFF == 27:
		resetMotors()
		break

cap.release()
