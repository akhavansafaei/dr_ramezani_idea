"""
Face Detection Module
Supports multiple backends: OpenCV (Haar/DNN), MTCNN, MediaPipe
"""
import cv2
import numpy as np
from deepface import DeepFace


class FaceDetector:
    """Face detection with multiple backend support"""

    def __init__(self, method='opencv', confidence=0.5, device='cpu'):
        self.method = method
        self.confidence = confidence
        self.device = device
        self._init_detector()

    def _init_detector(self):
        """Initialize face detector based on method"""
        if self.method == 'opencv':
            # Using OpenCV DNN face detector (pre-trained ResNet)
            self.detector_type = 'opencv_dnn'
            try:
                model_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                self.face_cascade = cv2.CascadeClassifier(model_path)
                print(f"✓ Face detector initialized: OpenCV Haar Cascade")
            except Exception as e:
                print(f"Warning: Could not load OpenCV cascade: {e}")
                self.face_cascade = None

        elif self.method == 'mtcnn':
            try:
                from mtcnn import MTCNN
                self.detector = MTCNN(device=self.device)
                print(f"✓ Face detector initialized: MTCNN")
            except ImportError:
                print("Warning: MTCNN not available, falling back to OpenCV")
                self.method = 'opencv'
                self._init_detector()

        elif self.method == 'mediapipe':
            try:
                import mediapipe as mp
                self.mp_face_detection = mp.solutions.face_detection
                self.detector = self.mp_face_detection.FaceDetection(
                    min_detection_confidence=self.confidence
                )
                print(f"✓ Face detector initialized: MediaPipe")
            except ImportError:
                print("Warning: MediaPipe not available, falling back to OpenCV")
                self.method = 'opencv'
                self._init_detector()

        elif self.method == 'retinaface':
            # Using DeepFace's RetinaFace backend
            print(f"✓ Face detector initialized: RetinaFace (DeepFace)")

    def detect_faces(self, frame):
        """
        Detect faces in frame
        Returns: list of (x, y, w, h) tuples
        """
        if self.method == 'opencv':
            return self._detect_opencv(frame)
        elif self.method == 'mtcnn':
            return self._detect_mtcnn(frame)
        elif self.method == 'mediapipe':
            return self._detect_mediapipe(frame)
        elif self.method == 'retinaface':
            return self._detect_retinaface(frame)
        return []

    def _detect_opencv(self, frame):
        """Detect faces using OpenCV Haar Cascade"""
        if self.face_cascade is None:
            return []

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Convert to list of tuples
        return [(int(x), int(y), int(w), int(h)) for (x, y, w, h) in faces]

    def _detect_mtcnn(self, frame):
        """Detect faces using MTCNN"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detections = self.detector.detect_faces(rgb_frame)

        faces = []
        for detection in detections:
            if detection['confidence'] >= self.confidence:
                x, y, w, h = detection['box']
                faces.append((x, y, w, h))

        return faces

    def _detect_mediapipe(self, frame):
        """Detect faces using MediaPipe"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.detector.process(rgb_frame)

        faces = []
        if results.detections:
            h, w = frame.shape[:2]
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                faces.append((x, y, width, height))

        return faces

    def _detect_retinaface(self, frame):
        """Detect faces using RetinaFace (via DeepFace)"""
        try:
            # DeepFace.extract_faces returns faces with regions
            face_objs = DeepFace.extract_faces(
                frame,
                detector_backend='retinaface',
                enforce_detection=False
            )

            faces = []
            for face_obj in face_objs:
                region = face_obj.get('facial_area', {})
                if region:
                    x = region.get('x', 0)
                    y = region.get('y', 0)
                    w = region.get('w', 0)
                    h = region.get('h', 0)
                    faces.append((x, y, w, h))

            return faces
        except Exception as e:
            return []

    def draw_faces(self, frame, faces, color=(0, 255, 0), thickness=2):
        """Draw bounding boxes around detected faces"""
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)
        return frame
