"""
Mask and Glasses Detection Module
Detects if person is wearing mask and/or glasses
"""
import cv2
import numpy as np


class MaskGlassesDetector:
    """Detect mask and glasses on faces"""

    def __init__(self, device='cpu'):
        self.device = device
        # Load Haar Cascade for eye detection (for glasses)
        try:
            eye_cascade_path = cv2.data.haarcascades + 'haarcascade_eye.xml'
            self.eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
        except Exception as e:
            print(f"Warning: Could not load eye cascade: {e}")
            self.eye_cascade = None

        print(f"✓ Mask & Glasses detector initialized")

    def detect(self, frame, face_location):
        """
        Detect mask and glasses
        Returns: dict with 'mask' and 'glasses' boolean values
        """
        x, y, w, h = face_location

        # Extract face ROI
        face_roi = frame[y:y+h, x:x+w]

        if face_roi.size == 0:
            return {'mask': False, 'glasses': False}

        # Detect glasses
        has_glasses = self._detect_glasses(face_roi)

        # Detect mask
        has_mask = self._detect_mask(face_roi)

        return {
            'mask': has_mask,
            'glasses': has_glasses
        }

    def _detect_glasses(self, face_roi):
        """
        Detect glasses using eye detection
        Logic: If eyes are partially obscured or eye detection fails in upper face region,
        glasses might be present
        """
        if self.eye_cascade is None:
            return False

        try:
            gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

            # Detect eyes in upper half of face
            h, w = gray.shape
            upper_face = gray[0:int(h*0.6), :]

            eyes = self.eye_cascade.detectMultiScale(
                upper_face,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(10, 10)
            )

            # Simple heuristic: check for distinct rectangular patterns in eye region
            # This is a simplified approach
            if len(eyes) >= 2:
                # Check brightness variance around eyes (glasses create different patterns)
                eye_regions_brightness = []
                for (ex, ey, ew, eh) in eyes[:2]:
                    eye_region = upper_face[ey:ey+eh, ex:ex+ew]
                    if eye_region.size > 0:
                        brightness = np.mean(eye_region)
                        eye_regions_brightness.append(brightness)

                # If brightness is relatively uniform, might indicate glasses reflection
                if len(eye_regions_brightness) == 2:
                    brightness_diff = abs(eye_regions_brightness[0] - eye_regions_brightness[1])
                    # High brightness might indicate glasses reflection
                    avg_brightness = np.mean(eye_regions_brightness)
                    if avg_brightness > 120 and brightness_diff < 30:
                        return True

            return False

        except Exception as e:
            return False

    def _detect_mask(self, face_roi):
        """
        Detect mask using color and position analysis
        Logic: Masks typically cover lower part of face and have specific color patterns
        """
        try:
            h, w = face_roi.shape[:2]

            # Focus on lower half of face (where mask would be)
            lower_face = face_roi[int(h*0.5):, :]

            if lower_face.size == 0:
                return False

            # Convert to different color spaces for analysis
            hsv = cv2.cvtColor(lower_face, cv2.COLOR_BGR2HSV)
            gray = cv2.cvtColor(lower_face, cv2.COLOR_BGR2GRAY)

            # Check for uniform color patterns (masks are often single color)
            # Calculate color variance
            h_variance = np.var(hsv[:, :, 0])
            s_variance = np.var(hsv[:, :, 1])

            # Low variance in hue might indicate uniform color (mask)
            # Also check for specific color ranges common in masks

            # Check for white/blue masks (common medical masks)
            white_mask = cv2.inRange(hsv, np.array([0, 0, 150]), np.array([180, 50, 255]))
            blue_mask = cv2.inRange(hsv, np.array([90, 50, 50]), np.array([130, 255, 255]))

            white_pixels = np.count_nonzero(white_mask)
            blue_pixels = np.count_nonzero(blue_mask)
            total_pixels = lower_face.shape[0] * lower_face.shape[1]

            # If significant portion is white or blue, likely a mask
            if (white_pixels / total_pixels) > 0.4 or (blue_pixels / total_pixels) > 0.3:
                return True

            # Check edges - masks create distinct edge patterns
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.count_nonzero(edges) / total_pixels

            # High edge density in lower face might indicate mask edges
            if edge_density > 0.15 and h_variance < 500:
                return True

            return False

        except Exception as e:
            return False

    def batch_detect(self, frame, face_locations):
        """
        Detect mask and glasses for multiple faces
        Returns: list of dicts
        """
        results = []
        for face_loc in face_locations:
            result = self.detect(frame, face_loc)
            results.append(result)
        return results

    def draw_attributes(self, frame, face_location, has_mask, has_glasses, font_scale=0.5):
        """Draw mask and glasses indicators on frame"""
        x, y, w, h = face_location

        # Prepare text
        attributes = []
        if has_mask:
            attributes.append("😷 Mask")
        if has_glasses:
            attributes.append("👓 Glasses")

        if not attributes:
            return frame

        text = ", ".join(attributes)

        # Draw text
        font = cv2.FONT_HERSHEY_SIMPLEX
        (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, 1)

        # Position on the right side of face box
        text_x = x + w + 5
        text_y = y + h // 2

        # Ensure within frame bounds
        if text_x + text_w > frame.shape[1]:
            text_x = x - text_w - 5

        # Background rectangle
        cv2.rectangle(frame,
                     (text_x - 2, text_y - text_h - 2),
                     (text_x + text_w + 2, text_y + 2),
                     (0, 0, 0),
                     -1)

        # Text
        color = (0, 255, 255)  # Yellow
        cv2.putText(frame, text,
                   (text_x, text_y),
                   font, font_scale, color, 1, cv2.LINE_AA)

        return frame
