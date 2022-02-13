import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
	max_num_hands=1,
	min_detection_confidence=0.5,
	min_tracking_confidence=0.5)

def processHand(image):
	results = hands.process(image)

	if results.multi_hand_landmarks:
		hand_landmarks = results.multi_hand_landmarks[0]
		
		return hand_landmarks
	else:
		return None

def drawHandLandmarks(bgrIm, landmarkSet):
	mp_drawing.draw_landmarks(
		bgrIm,
		landmarkSet,
		mp_hands.HAND_CONNECTIONS)
