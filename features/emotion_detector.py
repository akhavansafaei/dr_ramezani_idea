"""
Emotion Detection Module
Detects emotions: happy, sad, angry, surprise, neutral, etc.
"""
import cv2
import numpy as np
from deepface import DeepFace


class EmotionDetector:
    """Detect emotions from faces"""

    def __init__(self, device='cpu'):
        self.device = device
        # Emotion labels mapping
        self.emotion_emoji = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😠',
            'surprise': '😲',
            'fear': '😨',
            'disgust': '🤢',
            'neutral': '😐'
        }
        print(f"✓ Emotion detector initialized")

    def detect_emotion(self, frame, face_location):
        """
        Detect emotion for a face
        Returns: dict with 'emotion' and 'confidence'
        """
        x, y, w, h = face_location

        # Extract face ROI with padding
        padding = 20
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(frame.shape[1], x + w + padding)
        y2 = min(frame.shape[0], y + h + padding)

        face_roi = frame[y1:y2, x1:x2]

        if face_roi.size == 0:
            return {'emotion': None, 'confidence': 0}

        try:
            # Analyze using DeepFace
            result = DeepFace.analyze(
                face_roi,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend='opencv',
                silent=True
            )

            # DeepFace may return a list or dict
            if isinstance(result, list):
                result = result[0]

            emotion = result.get('dominant_emotion', None)
            emotion_scores = result.get('emotion', {})
            confidence = emotion_scores.get(emotion, 0) if emotion else 0

            return {
                'emotion': emotion,
                'confidence': confidence,
                'scores': emotion_scores
            }

        except Exception as e:
            return {'emotion': None, 'confidence': 0}

    def batch_detect(self, frame, face_locations):
        """
        Detect emotions for multiple faces
        Returns: list of emotion dicts
        """
        results = []
        for face_loc in face_locations:
            result = self.detect_emotion(frame, face_loc)
            results.append(result)
        return results

    def draw_emotion(self, frame, face_location, emotion, confidence=None, font_scale=0.6):
        """Draw emotion label on frame"""
        if emotion is None:
            return frame

        x, y, w, h = face_location

        # Prepare text
        emoji = self.emotion_emoji.get(emotion, '')
        if confidence:
            text = f"{emotion} {emoji} ({confidence:.0f}%)"
        else:
            text = f"{emotion} {emoji}"

        # Draw text background
        font = cv2.FONT_HERSHEY_SIMPLEX
        (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, 1)

        # Position below the face box
        text_x = x
        text_y = y + h + 20

        # Ensure text stays within frame
        if text_y + text_h > frame.shape[0]:
            text_y = y - 10

        # Background rectangle
        cv2.rectangle(frame,
                     (text_x, text_y - text_h - 4),
                     (text_x + text_w + 4, text_y + 4),
                     (0, 0, 0),
                     -1)

        # Text
        color = self._get_emotion_color(emotion)
        cv2.putText(frame, text,
                   (text_x + 2, text_y),
                   font, font_scale, color, 1, cv2.LINE_AA)

        return frame

    def _get_emotion_color(self, emotion):
        """Get color based on emotion"""
        color_map = {
            'happy': (0, 255, 0),      # Green
            'sad': (255, 0, 0),         # Blue
            'angry': (0, 0, 255),       # Red
            'surprise': (255, 255, 0),  # Cyan
            'fear': (255, 0, 255),      # Magenta
            'disgust': (0, 165, 255),   # Orange
            'neutral': (200, 200, 200)  # Gray
        }
        return color_map.get(emotion, (255, 255, 255))
