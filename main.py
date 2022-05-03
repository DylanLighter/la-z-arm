#!/usr/bin/env python3

import cv2
import os
import sys

import joints
import hands
import pose
import wrist

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # cls for Windows (for testing off rig)
        command = 'cls'
    os.system(command)

def readFrame(cap):
	success, image = cap.read()
	if not success:
		print("Ignoring empty camera frame.")
		# If loading a video, use 'break' instead of 'continue'.
		return
	
	image.flags.writeable = False
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	
	hand_landmarks = hands.processHand(image)
	pose_landmarks = pose.processPose(image)

	clearConsole()

	if hand_landmarks: handlm = hand_landmarks.landmark
	if pose_landmarks: poselm = pose_landmarks.landmark
	
	if reportOnly:
		if hand_landmarks:
			print(joints.getJointDataString(handlm))
			if pose_landmarks:
				print(f"Wrist: {wrist.wrist.getCurlPercentage(poselm, handlm)}")
				print(f"%: {wrist.wrist.getCurlAngle(poselm, handlm)}")
	else:
		if hand_landmarks:
			for i in range(5):
				motors.rotateJoint(i, joints.fingers[i].getCurlPercentage(handlm))
			if pose_landmarks:
				motors.rotateJoint(5, wrist.wrist.getCurlPercentage(poselm, handlm))
		else:
			print('No hand detected.')

	image.flags.writeable = True
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

	hands.drawHandLandmarks(image, hand_landmarks)
	pose.drawPoseLandmarks(image, pose_landmarks)

	# Flip the image horizontally for a selfie-view display.
	image = cv2.flip(image, 1)

	cv2.imshow('MediaPipe Hands', image)

if __name__ == "__main__":
	cap = cv2.VideoCapture(0)

	# Use first argument to decide to report only
	# Always use report-only if in Windows
	reportOnly = os.name in ('nt', 'dos') or any(x in sys.argv for x in ["-r", "--report"])

	if not reportOnly:
		import motors

	while cap.isOpened():
		readFrame(cap)
		if cv2.waitKey(5) & 0xFF == 27:
			motors.resetMotors()
			break

	cap.release()
