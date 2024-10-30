# x3gesture_controller.py
# Developer: X3NIDE
# GitHub: https://github.com/mubbashirulislam

import cv2
import mediapipe as mp
import time
import math
import subprocess
import logging
from typing import Tuple, List, Any
import numpy as np

class X3GestureController:
    """
    A controller class to detect hand gestures using MediaPipe and trigger
    automation actions on a PC when a specific gesture (e.g., fist) is detected.
    """

    def __init__(self, camera_index: int, high_resolution: bool, gesture_cooldown: float = 1.0, action_callback=None):
        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        # Initialize MediaPipe hands solution
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        # Camera setup
        self.camera_index = camera_index
        self.high_resolution = high_resolution
        self.cap = None
        self.setup_camera()

        # Gesture parameters
        self.last_gesture_time = time.time()
        self.gesture_cooldown = gesture_cooldown
        self.action_callback = action_callback  # Callback function for automation

        # Gesture state for tracking detections across frames
        self.gesture_state = {
            'fist_detected': False,
            'consecutive_detections': 0,
            'required_consecutive_detections': 3
        }

        # Define indices for finger and thumb landmarks
        self.FINGER_TIPS = [8, 12, 16, 20]
        self.FINGER_PIPS = [6, 10, 14, 18]
        self.THUMB_TIP = 4
        self.THUMB_IP = 3

    def setup_camera(self) -> None:
        """Initialize the camera with specified resolution and check for errors."""
        try:
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                raise ValueError("Failed to open camera")
            self.set_camera_resolution(self.high_resolution)

            # Test frame capture to confirm the camera is functional
            ret, frame = self.cap.read()
            if not ret or frame is None:
                raise ValueError("Failed to capture test frame")
            self.logger.info("Camera initialized successfully")

        except Exception as e:
            self.logger.error(f"Camera initialization failed: {str(e)}")
            raise

    def set_camera_resolution(self, high_res: bool) -> None:
        """Set camera resolution to high or low based on user preference."""
        width, height = (1280, 720) if high_res else (640, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.logger.info(f"Camera resolution set to {'high' if high_res else 'low'}")

    def calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two points."""
        return math.hypot(point1[0] - point2[0], point1[1] - point2[1])

    def is_finger_closed(self, landmarks: List[Tuple[float, float]], tip_idx: int, pip_idx: int) -> bool:
        """Check if a finger is closed based on the position of its landmarks."""
        if tip_idx == self.THUMB_TIP:
            thumb_tip = landmarks[self.THUMB_TIP]
            index_base = landmarks[5]
            return self.calculate_distance(thumb_tip, index_base) < 0.1
        return landmarks[tip_idx][1] > landmarks[pip_idx][1]

    def detect_fist(self, landmarks: List[Any]) -> bool:
        """Detect if the hand is making a fist gesture by checking if all fingers are closed."""
        landmarks_2d = [(lm.x, lm.y) for lm in landmarks]
        fingers_closed = [self.is_finger_closed(landmarks_2d, tip, pip) for tip, pip in zip(self.FINGER_TIPS, self.FINGER_PIPS)]
        return all(fingers_closed)

    def update_gesture_state(self, is_fist: bool) -> bool:
        """Track gesture state across frames and return True when gesture is detected consistently."""
        if is_fist:
            self.gesture_state['consecutive_detections'] += 1
        else:
            self.gesture_state['consecutive_detections'] = 0
            self.gesture_state['fist_detected'] = False

        if (self.gesture_state['consecutive_detections'] >=
            self.gesture_state['required_consecutive_detections'] and
            not self.gesture_state['fist_detected']):
            self.gesture_state['fist_detected'] = True
            return True
        return False

    def trigger_automation(self) -> None:
        """Invoke the selected automation action when the fist gesture is detected."""
        if self.action_callback and time.time() - self.last_gesture_time > self.gesture_cooldown:
            self.logger.info("Fist gesture detected - triggering action")
            self.action_callback()
            self.last_gesture_time = time.time()

    def run(self) -> None:
        """Main loop for capturing frames, detecting gestures, and triggering actions."""
        try:
            self.logger.info("Starting main processing loop")
            while self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    self.logger.error("Failed to capture frame")
                    break

                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(frame_rgb)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                        is_fist = self.detect_fist(hand_landmarks.landmark)
                        if self.update_gesture_state(is_fist):
                            self.trigger_automation()
                cv2.imshow("X3Gesture Control", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            self.logger.error(f"Runtime error: {str(e)}")
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Release all resources and close OpenCV windows."""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
