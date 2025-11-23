"""
Computer Vision Project - Main Application
Budget-friendly multi-feature face analysis system

Features:
- Face detection with bounding boxes
- Person counting
- Unique person tracking
- Age detection
- Gender detection
- Emotion detection
- Pose detection (sitting/standing)
- Mask and glasses detection

Hardware: Auto-detects GPU/CPU, optimizes for performance
"""

import cv2
import argparse
import time
from config import Config
from utils.device_utils import detect_device, get_device_info
from utils.fps_monitor import FPSMonitor
from features.face_detector import FaceDetector
from features.person_tracker import PersonTracker
from features.age_gender_detector import AgeGenderDetector
from features.emotion_detector import EmotionDetector
from features.pose_detector import PoseDetector
from features.mask_glasses_detector import MaskGlassesDetector


class CVApplication:
    """Main Computer Vision Application"""

    def __init__(self, config):
        self.config = config
        self.running = False
        self.frame_count = 0

        # Initialize device
        if config.device == 'auto':
            self.device = detect_device()
        else:
            self.device = config.device

        print(f"\n{'='*60}")
        print(f"Computer Vision System - Budget Friendly Edition")
        print(f"{'='*60}")

        # Initialize FPS monitor
        self.fps_monitor = FPSMonitor(
            target_fps=config.target_fps,
            window_size=30
        )

        # Initialize feature modules
        print(f"\nInitializing feature modules...")
        self.face_detector = FaceDetector(
            method=config.face_detection_method,
            confidence=config.face_detection_confidence,
            device=self.device
        )

        self.person_tracker = None
        if config.is_enabled('unique_tracking'):
            self.person_tracker = PersonTracker(
                database_path=config.face_database_path,
                similarity_threshold=config.face_similarity_threshold
            )

        self.age_gender_detector = None
        if config.is_enabled('age_detection') or config.is_enabled('gender_detection'):
            self.age_gender_detector = AgeGenderDetector(device=self.device)

        self.emotion_detector = None
        if config.is_enabled('emotion_detection'):
            self.emotion_detector = EmotionDetector(device=self.device)

        self.pose_detector = None
        if config.is_enabled('pose_detection'):
            self.pose_detector = PoseDetector(device=self.device)

        self.mask_glasses_detector = None
        if config.is_enabled('mask_glasses_detection'):
            self.mask_glasses_detector = MaskGlassesDetector(device=self.device)

        print(f"\n✓ System initialized successfully!")
        self._print_feature_status()

    def _print_feature_status(self):
        """Print current feature status"""
        print(f"\nFeature Status:")
        print(f"{'-'*60}")
        for feature_name, feature_info in sorted(
            self.config.features.items(),
            key=lambda x: x[1]['priority']
        ):
            status = "✓ ENABLED " if feature_info['enabled'] else "✗ DISABLED"
            print(f"{status} | {feature_info['name']}")
        print(f"{'-'*60}")

    def process_frame(self, frame):
        """Process a single frame with enabled features"""

        # Resize frame for performance
        if self.config.resize_width:
            height, width = frame.shape[:2]
            if width > self.config.resize_width:
                scale = self.config.resize_width / width
                frame = cv2.resize(frame, None, fx=scale, fy=scale)

        display_frame = frame.copy()

        # Feature 1: Face Detection (always needed for other features)
        faces = []
        if self.config.is_enabled('face_detection'):
            faces = self.face_detector.detect_faces(frame)

            # Draw bounding boxes
            for face in faces:
                x, y, w, h = face
                cv2.rectangle(display_frame, (x, y), (x + w, y + h),
                            (0, 255, 0), self.config.box_thickness)

        # Feature 2: Person Count
        person_count = len(faces)

        # Feature 3: Unique Person Tracking
        unique_count = 0
        if self.config.is_enabled('unique_tracking') and self.person_tracker and len(faces) > 0:
            for face in faces:
                is_new, person_id = self.person_tracker.identify_or_register_face(frame, face)
            unique_count = self.person_tracker.get_unique_count()

        # Process each face for remaining features
        for i, face in enumerate(faces):
            x, y, w, h = face
            y_offset = y  # Track vertical position for labels

            # Feature 4 & 5: Age and Gender Detection
            if (self.config.is_enabled('age_detection') or
                self.config.is_enabled('gender_detection')) and self.age_gender_detector:

                result = self.age_gender_detector.analyze_face(frame, face)
                age = result.get('age') if self.config.is_enabled('age_detection') else None
                gender = result.get('gender') if self.config.is_enabled('gender_detection') else None

                if age or gender:
                    self.age_gender_detector.draw_age_gender(
                        display_frame, face, age, gender, self.config.font_scale
                    )

            # Feature 6: Emotion Detection
            if self.config.is_enabled('emotion_detection') and self.emotion_detector:
                emotion_result = self.emotion_detector.detect_emotion(frame, face)
                emotion = emotion_result.get('emotion')
                confidence = emotion_result.get('confidence')

                if emotion:
                    self.emotion_detector.draw_emotion(
                        display_frame, face, emotion, confidence, self.config.font_scale
                    )

            # Feature 7: Pose Detection
            if self.config.is_enabled('pose_detection') and self.pose_detector:
                pose = self.pose_detector.detect_pose(frame, face)
                if pose:
                    self.pose_detector.draw_pose(
                        display_frame, pose, face, self.config.font_scale
                    )

            # Feature 8: Mask and Glasses Detection
            if self.config.is_enabled('mask_glasses_detection') and self.mask_glasses_detector:
                mg_result = self.mask_glasses_detector.detect(frame, face)
                has_mask = mg_result.get('mask', False)
                has_glasses = mg_result.get('glasses', False)

                if has_mask or has_glasses:
                    self.mask_glasses_detector.draw_attributes(
                        display_frame, face, has_mask, has_glasses, self.config.font_scale - 0.1
                    )

        # Draw statistics
        self._draw_statistics(display_frame, person_count, unique_count)

        return display_frame

    def _draw_statistics(self, frame, person_count, unique_count):
        """Draw statistics overlay"""
        h, w = frame.shape[:2]

        # Create semi-transparent overlay for stats
        overlay = frame.copy()
        stats_height = 120 if unique_count > 0 else 100

        cv2.rectangle(overlay, (10, 10), (300, 10 + stats_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

        # Draw statistics
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        color = (255, 255, 255)
        y_pos = 35

        # FPS
        if self.config.show_fps:
            fps = self.fps_monitor.get_fps()
            fps_text = f"FPS: {fps:.1f}"
            fps_color = (0, 255, 0) if fps >= self.config.target_fps else (0, 165, 255)
            cv2.putText(frame, fps_text, (20, y_pos), font, font_scale, fps_color, 2)
            y_pos += 25

        # Device
        if self.config.show_device:
            device_text = f"Device: {self.device.upper()}"
            cv2.putText(frame, device_text, (20, y_pos), font, font_scale, color, 2)
            y_pos += 25

        # Person count
        if self.config.is_enabled('person_count'):
            count_text = f"People: {person_count}"
            cv2.putText(frame, count_text, (20, y_pos), font, font_scale, color, 2)
            y_pos += 25

        # Unique count
        if self.config.is_enabled('unique_tracking') and unique_count > 0:
            unique_text = f"Unique: {unique_count}"
            cv2.putText(frame, unique_text, (20, y_pos), font, font_scale, (0, 255, 255), 2)
            y_pos += 25

    def auto_optimize(self):
        """Auto-optimize features based on FPS"""
        if not self.config.auto_optimize:
            return

        # Check if we should disable a feature
        if self.fps_monitor.should_disable_feature():
            disabled = self.config.disable_lowest_priority_feature()
            if disabled:
                feature_name = self.config.features[disabled]['name']
                print(f"\n⚠ Auto-optimization: Disabled '{feature_name}' to improve FPS")
                self.fps_monitor.reset()  # Reset to measure new performance

        # Check if we can enable a feature
        elif self.fps_monitor.should_enable_feature():
            enabled = self.config.enable_highest_priority_disabled_feature()
            if enabled:
                feature_name = self.config.features[enabled]['name']
                print(f"\n✓ Auto-optimization: Enabled '{feature_name}' (FPS stable)")
                self.fps_monitor.reset()  # Reset to measure new performance

    def run(self, source=0):
        """Run the CV application"""
        # Open video source
        cap = cv2.VideoCapture(source)

        if not cap.isOpened():
            print(f"Error: Could not open video source: {source}")
            return

        print(f"\n{'='*60}")
        print(f"Starting video processing...")
        print(f"Press 'q' to quit, 's' to screenshot, 'r' to reset tracking")
        print(f"{'='*60}\n")

        self.running = True

        try:
            while self.running:
                ret, frame = cap.read()

                if not ret:
                    print("End of video or cannot read frame")
                    break

                # Process frame
                self.frame_count += 1

                # Skip frames if configured
                if self.frame_count % self.config.frame_skip != 0:
                    continue

                processed_frame = self.process_frame(frame)

                # Update FPS
                fps = self.fps_monitor.update()

                # Auto-optimize every 30 frames
                if self.frame_count % 30 == 0:
                    self.auto_optimize()

                # Display
                cv2.imshow('Computer Vision System', processed_frame)

                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF

                if key == ord('q'):
                    print("\nQuitting...")
                    break
                elif key == ord('s'):
                    filename = f"screenshot_{int(time.time())}.jpg"
                    cv2.imwrite(filename, processed_frame)
                    print(f"\n✓ Screenshot saved: {filename}")
                elif key == ord('r'):
                    if self.person_tracker:
                        self.person_tracker.reset_database()
                        print("\n✓ Person tracking database reset")

        except KeyboardInterrupt:
            print("\n\nInterrupted by user")

        finally:
            cap.release()
            cv2.destroyAllWindows()
            print(f"\n{'='*60}")
            print(f"Session Statistics:")
            print(f"  Total frames processed: {self.frame_count}")
            print(f"  Average FPS: {self.fps_monitor.get_fps():.1f}")
            if self.person_tracker:
                print(f"  Unique people detected: {self.person_tracker.get_unique_count()}")
            print(f"{'='*60}\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Budget-friendly Computer Vision System'
    )
    parser.add_argument(
        '--source',
        type=str,
        default='0',
        help='Video source (0 for webcam, or path to video file)'
    )
    parser.add_argument(
        '--device',
        type=str,
        default='auto',
        choices=['auto', 'cpu', 'cuda'],
        help='Device to use (auto, cpu, or cuda)'
    )
    parser.add_argument(
        '--auto-optimize',
        action='store_true',
        help='Enable auto-optimization to maintain target FPS'
    )
    parser.add_argument(
        '--target-fps',
        type=int,
        default=15,
        help='Target FPS for auto-optimization (default: 15)'
    )
    parser.add_argument(
        '--disable',
        type=str,
        nargs='+',
        help='Features to disable (e.g., --disable age_detection emotion_detection)'
    )

    args = parser.parse_args()

    # Create configuration
    config = Config()
    config.device = args.device
    config.auto_optimize = args.auto_optimize
    config.target_fps = args.target_fps

    # Disable requested features
    if args.disable:
        for feature in args.disable:
            if feature in config.features:
                config.disable_feature(feature)
                print(f"Disabled feature: {feature}")

    # Parse source (convert to int if it's a number)
    try:
        source = int(args.source)
    except ValueError:
        source = args.source

    # Create and run application
    app = CVApplication(config)
    app.run(source=source)


if __name__ == '__main__':
    main()
