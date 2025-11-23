"""
Age and Gender Detection Module
Uses DeepFace for analysis
"""
import cv2
import numpy as np
from deepface import DeepFace


class AgeGenderDetector:
    """Detect age and gender from faces"""

    def __init__(self, device='cpu'):
        self.device = device
        print(f"✓ Age & Gender detector initialized")

    def analyze_face(self, frame, face_location):
        """
        Analyze age and gender for a face
        Returns: dict with 'age' and 'gender' keys
        """
        x, y, w, h = face_location

        # Extract face ROI with some padding
        padding = 20
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(frame.shape[1], x + w + padding)
        y2 = min(frame.shape[0], y + h + padding)

        face_roi = frame[y1:y2, x1:x2]

        if face_roi.size == 0:
            return {'age': None, 'gender': None}

        try:
            # Analyze using DeepFace
            result = DeepFace.analyze(
                face_roi,
                actions=['age', 'gender'],
                enforce_detection=False,
                detector_backend='opencv',
                silent=True
            )

            # DeepFace may return a list or dict
            if isinstance(result, list):
                result = result[0]

            age = result.get('age', None)
            gender = result.get('dominant_gender', None)

            return {
                'age': int(age) if age is not None else None,
                'gender': gender
            }

        except Exception as e:
            return {'age': None, 'gender': None}

    def batch_analyze(self, frame, face_locations):
        """
        Analyze multiple faces
        Returns: list of dicts with 'age' and 'gender'
        """
        results = []
        for face_loc in face_locations:
            result = self.analyze_face(frame, face_loc)
            results.append(result)
        return results

    def draw_age_gender(self, frame, face_location, age, gender, font_scale=0.6):
        """Draw age and gender labels on frame"""
        x, y, w, h = face_location

        # Prepare text
        text_parts = []
        if age is not None:
            text_parts.append(f"Age: {age}")
        if gender is not None:
            text_parts.append(f"{gender}")

        text = ", ".join(text_parts)

        if text:
            # Draw text background
            font = cv2.FONT_HERSHEY_SIMPLEX
            (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, 1)

            # Position above the face box
            text_x = x
            text_y = y - 10

            # Background rectangle
            cv2.rectangle(frame,
                         (text_x, text_y - text_h - 4),
                         (text_x + text_w + 4, text_y + 4),
                         (0, 0, 0),
                         -1)

            # Text
            cv2.putText(frame, text,
                       (text_x + 2, text_y),
                       font, font_scale, (0, 255, 255), 1, cv2.LINE_AA)

        return frame
