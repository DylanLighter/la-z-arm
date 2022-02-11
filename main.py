import cv2

from finger_angle import *
from motors import *
from hands import *
from pose import *

cap = cv2.VideoCapture(0)

while cap.isOpened():
	success, image = cap.read()
	if not success:
		print("Ignoring empty camera frame.")
		# If loading a video, use 'break' instead of 'continue'.
		continue
	
	hand_landmarks = processHand(image)

	if not hand_landmarks:
		continue
	
	landmark = landmarks.landmark

	print(getFingerDataString(landmark))
	rotateFinger(0, getCurlPercentage(landmark, 0))
	rotateFinger(1, getCurlPercentage(landmark, 1))

	# Flip the image horizontally for a selfie-view display.
	image = cv2.flip(image, 1)

	cv2.imshow('MediaPipe Hands', image)

	if cv2.waitKey(5) & 0xFF == 27:
		break

cap.release()
