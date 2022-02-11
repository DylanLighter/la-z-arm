import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
		min_detection_confidence=0.5,
		min_tracking_confidence=0.5)

def processPose(image):
	# To improve performance, optionally mark the image as not writeable to
	# pass by reference.
	image.flags.writeable = False
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	results = pose.process(image)

	# Draw the pose annotation on the image.
	image.flags.writeable = True
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

	mp_drawing.draw_landmarks(
		image,
		results.pose_landmarks.landmark,
		mp_pose.POSE_CONNECTIONS)
