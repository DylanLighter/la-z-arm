import cv2
import os

from finger_angle import *
from motors import *
from hands import *
from pose import *

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # cls for Windows (for testing off rig)
        command = 'cls'
    os.system(command)

cap = cv2.VideoCapture(0)

while cap.isOpened():
	success, image = cap.read()
	if not success:
		print("Ignoring empty camera frame.")
		# If loading a video, use 'break' instead of 'continue'.
		continue
	
	image.flags.writeable = False
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	
	hand_landmarks = processHand(image)

	clearConsole()

	if hand_landmarks:
		landmark = hand_landmarks.landmark
		print(getFingerDataString(landmark))
		rotateFinger(0, getCurlPercentage(landmark, 0))
		rotateFinger(1, getCurlPercentage(landmark, 1))
	else:
		print('No hand detected.')

	image.flags.writeable = True
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

	drawHandLandmarks(image, hand_landmarks)

	# Flip the image horizontally for a selfie-view display.
	image = cv2.flip(image, 1)

	cv2.imshow('MediaPipe Hands', image)

	if cv2.waitKey(5) & 0xFF == 27:
		break

cap.release()
