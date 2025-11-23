"""
Pose Detection Module
Detects sitting/standing poses using MediaPipe or simple heuristics
"""
import cv2
import numpy as np


class PoseDetector:
    """Detect sitting/standing poses"""

    def __init__(self, device='cpu'):
        self.device = device
        self.pose_detector = None
        self.use_mediapipe = False

        # Try to initialize MediaPipe
        try:
            import mediapipe as mp
            self.mp_pose = mp.solutions.pose
            self.pose_detector = self.mp_pose.Pose(
                static_image_mode=False,
                model_complexity=0,  # Lightest model
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            self.use_mediapipe = True
            print(f"✓ Pose detector initialized: MediaPipe")
        except ImportError:
            print(f"✓ Pose detector initialized: Heuristic method (MediaPipe not available)")

    def detect_pose(self, frame, face_location=None):
        """
        Detect if person is sitting or standing
        Returns: 'sitting', 'standing', or None
        """
        if self.use_mediapipe:
            return self._detect_mediapipe(frame)
        else:
            # Fallback: use simple heuristics based on face position
            return self._detect_heuristic(frame, face_location)

    def _detect_mediapipe(self, frame):
        """Detect pose using MediaPipe"""
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose_detector.process(rgb_frame)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                # Get key points
                nose = landmarks[self.mp_pose.PoseLandmark.NOSE.value]
                left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
                right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
                left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
                right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]
                left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
                right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]

                # Calculate hip position (average)
                hip_y = (left_hip.y + right_hip.y) / 2

                # Calculate knee position (average)
                knee_y = (left_knee.y + right_knee.y) / 2

                # Calculate ankle position (average)
                ankle_y = (left_ankle.y + right_ankle.y) / 2

                # Heuristic: if hips are significantly above knees and knees are bent
                # it's likely sitting
                hip_knee_dist = knee_y - hip_y
                knee_ankle_dist = ankle_y - knee_y

                # Check visibility
                if (left_hip.visibility > 0.5 and right_hip.visibility > 0.5 and
                    left_knee.visibility > 0.5 and right_knee.visibility > 0.5):

                    # If hip-knee distance is small and knee-ankle is small, likely sitting
                    if hip_knee_dist < 0.2 and knee_ankle_dist < 0.15:
                        return 'sitting'
                    # If hip is higher up and full leg is visible, likely standing
                    elif hip_knee_dist > 0.15 and ankle_y > 0.7:
                        return 'standing'

            return None

        except Exception as e:
            return None

    def _detect_heuristic(self, frame, face_location):
        """
        Simple heuristic: if face is in upper part of frame, likely standing
        If in middle/lower part, likely sitting
        """
        if face_location is None:
            return None

        x, y, w, h = face_location
        frame_height = frame.shape[0]

        # Calculate face center Y position
        face_center_y = y + h / 2

        # Normalize to 0-1
        normalized_y = face_center_y / frame_height

        # Simple heuristic
        if normalized_y < 0.4:
            return 'standing'
        elif normalized_y > 0.5:
            return 'sitting'
        else:
            return None

    def draw_pose(self, frame, pose, face_location=None, font_scale=0.6):
        """Draw pose label on frame"""
        if pose is None:
            return frame

        # Determine position for text
        if face_location:
            x, y, w, h = face_location
            text_x = x + w + 10
            text_y = y + 20
        else:
            text_x = 10
            text_y = frame.shape[0] - 30

        # Prepare text
        text = f"Pose: {pose}"
        color = (255, 128, 0) if pose == 'standing' else (128, 128, 255)

        # Draw text background
        font = cv2.FONT_HERSHEY_SIMPLEX
        (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, 1)

        cv2.rectangle(frame,
                     (text_x, text_y - text_h - 4),
                     (text_x + text_w + 4, text_y + 4),
                     (0, 0, 0),
                     -1)

        # Text
        cv2.putText(frame, text,
                   (text_x + 2, text_y),
                   font, font_scale, color, 1, cv2.LINE_AA)

        return frame

    def draw_skeleton(self, frame, landmarks=None):
        """Draw pose skeleton on frame (if using MediaPipe)"""
        if not self.use_mediapipe or landmarks is None:
            return frame

        # This would draw the full skeleton - simplified for performance
        return frame
