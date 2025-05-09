import cv2 as cv
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

class ImageProcessor:
    def __init__(self, video_width=640, video_height=480):
        self.video_width = video_width
        self.video_height = video_height
        self.vid = cv.VideoCapture(0)
        self.hands = mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def capture_frame(self):
        """Capture and preprocess a frame from the webcam."""
        ret, frame = self.vid.read()
        if not ret:
            return None
        frame = cv.flip(frame, 1)
        frame = cv.resize(frame, (self.video_width, self.video_height))
        return frame

    def process_hands(self, frame):
        """Process the frame to detect hands using MediaPipe."""
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results

    def draw_landmarks(self, frame, results):
        """Draw hand landmarks on the frame."""
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
        return frame

    def get_hand_move(self, hand_landmarks):
        """Detect the hand gesture (rock, paper, scissors)."""
        landmarks = hand_landmarks.landmark
        threshold = 0.05

        # Get finger positions
        index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
        index_pip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
        middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
        middle_pip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
        ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y
        ring_pip = landmarks[mp_hands.HandLandmark.RING_FINGER_PIP].y
        pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP].y
        pinky_pip = landmarks[mp_hands.HandLandmark.PINKY_PIP].y
        thumb_tip_x = landmarks[mp_hands.HandLandmark.THUMB_TIP].x
        thumb_ip_x = landmarks[mp_hands.HandLandmark.THUMB_IP].x
        wrist_x = landmarks[mp_hands.HandLandmark.WRIST].x

        # Check if thumb is extended
        is_right_hand = thumb_tip_x > wrist_x
        thumb_extended = (thumb_tip_x > thumb_ip_x) if is_right_hand else (thumb_tip_x < thumb_ip_x)

        # Check which fingers are extended
        index_extended = index_tip < index_pip - threshold
        middle_extended = middle_tip < middle_pip - threshold
        ring_extended = ring_tip < ring_pip - threshold
        pinky_extended = pinky_tip < pinky_pip - threshold

        # Gesture detection
        if not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return "rock"
        elif index_extended and middle_extended and not ring_extended and not pinky_extended:
            return "scissors"
        else:
            return "paper"

    def release(self):
        """Release the video capture."""
        self.vid.release()