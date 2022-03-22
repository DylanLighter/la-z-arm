#!/usr/bin/env python3

import cv2
import os
import sys

import joints
import motors
import hands
import pose

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # cls for Windows (for testing off rig)
        command = 'cls'
    os.system(command)

cap = cv2.VideoCapture(0)

# Use first argument to decide to report only
reportOnly = len(sys.argv) > 1 and (sys.argv[1] == "--report" or "-r")

while cap.isOpened():
	success, image = cap.read()
	if not success:
		print("Ignoring empty camera frame.")
		# If loading a video, use 'break' instead of 'continue'.
		continue
	
	image.flags.writeable = False
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	
	hand_landmarks = hands.processHand(image)
	pose_landmarks = pose.processPose(image)

	clearConsole()
	
	if reportOnly:
		if hand_landmarks:
			print(joints.getJointDataString(hand_landmarks.landmark))
	else:
		if hand_landmarks:
			landmark = hand_landmarks.landmark
			for i in range(5):
				motors.rotateJoint(i, joints.fingers[i].getCurlPercentage(landmark))
		else:
			print('No hand detected.')

	image.flags.writeable = True
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

	hands.drawHandLandmarks(image, hand_landmarks)
	pose.drawPoseLandmarks(image, pose_landmarks)

	# Flip the image horizontally for a selfie-view display.
	image = cv2.flip(image, 1)

	cv2.imshow('MediaPipe Hands', image)

	if cv2.waitKey(5) & 0xFF == 27:
		motors.resetMotors()
		break

cap.release()
