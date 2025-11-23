"""
Person Tracking Module
Tracks unique persons using face recognition
"""
import os
import pickle
import numpy as np
import cv2
from datetime import datetime


class PersonTracker:
    """Track unique persons using face embeddings"""

    def __init__(self, database_path='face_database', similarity_threshold=0.6):
        self.database_path = database_path
        self.similarity_threshold = similarity_threshold
        self.known_faces = []
        self.known_encodings = []
        self.face_count = 0

        # Create database directory
        os.makedirs(database_path, exist_ok=True)

        # Load existing database
        self._load_database()

    def _load_database(self):
        """Load known faces from database"""
        db_file = os.path.join(self.database_path, 'face_db.pkl')
        if os.path.exists(db_file):
            try:
                with open(db_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_encodings = data.get('encodings', [])
                    self.face_count = data.get('count', 0)
                print(f"✓ Loaded {self.face_count} known faces from database")
            except Exception as e:
                print(f"Warning: Could not load face database: {e}")

    def _save_database(self):
        """Save known faces to database"""
        db_file = os.path.join(self.database_path, 'face_db.pkl')
        try:
            data = {
                'encodings': self.known_encodings,
                'count': self.face_count
            }
            with open(db_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"Warning: Could not save face database: {e}")

    def get_face_encoding(self, frame, face_location):
        """
        Get face encoding using simple method (for low-budget systems)
        Uses histogram of oriented gradients (HOG) features
        """
        x, y, w, h = face_location

        # Extract face ROI
        face_roi = frame[y:y+h, x:x+w]

        if face_roi.size == 0:
            return None

        # Resize to standard size
        try:
            face_resized = cv2.resize(face_roi, (128, 128))

            # Convert to grayscale
            if len(face_resized.shape) == 3:
                face_gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)
            else:
                face_gray = face_resized

            # Compute simple feature vector (histogram + edges)
            # This is a lightweight alternative to deep learning embeddings
            hist = cv2.calcHist([face_gray], [0], None, [32], [0, 256])
            hist = hist.flatten()
            hist = hist / (hist.sum() + 1e-7)  # Normalize

            # Add edge features
            edges = cv2.Canny(face_gray, 50, 150)
            edge_hist = cv2.calcHist([edges], [0], None, [16], [0, 256])
            edge_hist = edge_hist.flatten()
            edge_hist = edge_hist / (edge_hist.sum() + 1e-7)

            # Combine features
            encoding = np.concatenate([hist, edge_hist])

            return encoding

        except Exception as e:
            return None

    def compute_similarity(self, encoding1, encoding2):
        """Compute cosine similarity between two encodings"""
        if encoding1 is None or encoding2 is None:
            return 0.0

        # Cosine similarity
        dot_product = np.dot(encoding1, encoding2)
        norm1 = np.linalg.norm(encoding1)
        norm2 = np.linalg.norm(encoding2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = dot_product / (norm1 * norm2)
        return similarity

    def identify_or_register_face(self, frame, face_location):
        """
        Identify if face is known, or register as new person
        Returns: (is_new, person_id)
        """
        encoding = self.get_face_encoding(frame, face_location)

        if encoding is None:
            return False, -1

        # Check against known faces
        if len(self.known_encodings) == 0:
            # First face
            self.known_encodings.append(encoding)
            self.face_count += 1
            self._save_face_image(frame, face_location, self.face_count)
            self._save_database()
            return True, self.face_count

        # Find best match
        similarities = [self.compute_similarity(encoding, known_enc)
                       for known_enc in self.known_encodings]
        best_match_idx = np.argmax(similarities)
        best_similarity = similarities[best_match_idx]

        if best_similarity >= self.similarity_threshold:
            # Known person
            return False, best_match_idx + 1
        else:
            # New person
            self.known_encodings.append(encoding)
            self.face_count += 1
            self._save_face_image(frame, face_location, self.face_count)
            self._save_database()
            return True, self.face_count

    def _save_face_image(self, frame, face_location, person_id):
        """Save face image to database"""
        x, y, w, h = face_location
        face_roi = frame[y:y+h, x:x+w]

        if face_roi.size > 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"person_{person_id:04d}_{timestamp}.jpg"
            filepath = os.path.join(self.database_path, filename)
            cv2.imwrite(filepath, face_roi)

    def get_unique_count(self):
        """Get count of unique persons"""
        return self.face_count

    def reset_database(self):
        """Reset the face database"""
        self.known_encodings = []
        self.face_count = 0
        self._save_database()
        print("✓ Face database reset")
