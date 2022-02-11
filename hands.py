import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
	max_num_hands=1,
	min_detection_confidence=0.5,
	min_tracking_confidence=0.5)

def processHand(image):
	image.flags.writeable = False
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	results = hands.process(image)

	image.flags.writeable = True
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

	if results.multi_hand_landmarks:
		hand_landmarks = results.multi_hand_landmarks[0]
		mp_drawing.draw_landmarks(
			image,
			hand_landmarks,
			mp_hands.HAND_CONNECTIONS)
		
		return hand_landmarks
	else:
		return None
