import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
		min_detection_confidence=0.5,
		min_tracking_confidence=0.5)

def processPose(image):
	return pose.process(image).pose_landmarks

def drawPoseLandmarks(bgrIm, landmarkSet):
	mp_drawing.draw_landmarks(
		bgrIm,
		landmarkSet,
		mp_pose.POSE_CONNECTIONS)
