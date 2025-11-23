"""
Modern Web Interface for Computer Vision System
Gradio-based interactive web application
"""

import gradio as gr
import cv2
import numpy as np
from config import Config
from utils.device_utils import detect_device, get_device_info
from utils.fps_monitor import FPSMonitor
from features.face_detector import FaceDetector
from features.person_tracker import PersonTracker
from features.age_gender_detector import AgeGenderDetector
from features.emotion_detector import EmotionDetector
from features.pose_detector import PoseDetector
from features.mask_glasses_detector import MaskGlassesDetector


class WebCVApp:
    """Web-based Computer Vision Application"""

    def __init__(self):
        self.config = Config()
        self.device = detect_device()
        self.fps_monitor = None
        self.detectors_initialized = False

        # Feature detectors
        self.face_detector = None
        self.person_tracker = None
        self.age_gender_detector = None
        self.emotion_detector = None
        self.pose_detector = None
        self.mask_glasses_detector = None

    def initialize_detectors(self):
        """Initialize all detectors"""
        if self.detectors_initialized:
            return

        print("Initializing detectors...")

        self.fps_monitor = FPSMonitor(
            target_fps=self.config.target_fps,
            window_size=30
        )

        self.face_detector = FaceDetector(
            method=self.config.face_detection_method,
            confidence=self.config.face_detection_confidence,
            device=self.device
        )

        if self.config.is_enabled('unique_tracking'):
            self.person_tracker = PersonTracker(
                database_path=self.config.face_database_path,
                similarity_threshold=self.config.face_similarity_threshold
            )

        if self.config.is_enabled('age_detection') or self.config.is_enabled('gender_detection'):
            self.age_gender_detector = AgeGenderDetector(device=self.device)

        if self.config.is_enabled('emotion_detection'):
            self.emotion_detector = EmotionDetector(device=self.device)

        if self.config.is_enabled('pose_detection'):
            self.pose_detector = PoseDetector(device=self.device)

        if self.config.is_enabled('mask_glasses_detection'):
            self.mask_glasses_detector = MaskGlassesDetector(device=self.device)

        self.detectors_initialized = True
        print("✓ Detectors initialized")

    def update_config(
        self,
        face_detection,
        person_count,
        unique_tracking,
        age_detection,
        gender_detection,
        emotion_detection,
        pose_detection,
        mask_glasses,
        auto_optimize,
        target_fps
    ):
        """Update configuration based on UI inputs"""
        # Update feature toggles
        features_map = {
            'face_detection': face_detection,
            'person_count': person_count,
            'unique_tracking': unique_tracking,
            'age_detection': age_detection,
            'gender_detection': gender_detection,
            'emotion_detection': emotion_detection,
            'pose_detection': pose_detection,
            'mask_glasses_detection': mask_glasses
        }

        for feature, enabled in features_map.items():
            if enabled:
                self.config.enable_feature(feature)
            else:
                self.config.disable_feature(feature)

        # Update performance settings
        self.config.auto_optimize = auto_optimize
        self.config.target_fps = int(target_fps)

        # Reinitialize detectors with new config
        self.detectors_initialized = False

    def process_frame(self, frame):
        """Process a single frame"""
        if frame is None:
            return None, "No frame to process"

        # Initialize detectors if needed
        self.initialize_detectors()

        # Convert RGB to BGR (OpenCV format)
        if len(frame.shape) == 3 and frame.shape[2] == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Resize for performance
        if self.config.resize_width:
            height, width = frame.shape[:2]
            if width > self.config.resize_width:
                scale = self.config.resize_width / width
                frame = cv2.resize(frame, None, fx=scale, fy=scale)

        display_frame = frame.copy()
        stats = []

        # Face detection
        faces = []
        if self.config.is_enabled('face_detection'):
            faces = self.face_detector.detect_faces(frame)
            for face in faces:
                x, y, w, h = face
                cv2.rectangle(display_frame, (x, y), (x + w, y + h),
                            (0, 255, 0), self.config.box_thickness)

        # Person count
        person_count = len(faces)
        stats.append(f"👥 **People Detected:** {person_count}")

        # Unique tracking
        unique_count = 0
        if self.config.is_enabled('unique_tracking') and self.person_tracker and len(faces) > 0:
            for face in faces:
                self.person_tracker.identify_or_register_face(frame, face)
            unique_count = self.person_tracker.get_unique_count()
            stats.append(f"🔍 **Unique People:** {unique_count}")

        # Process each face
        for i, face in enumerate(faces):
            face_stats = []

            # Age & Gender
            if (self.config.is_enabled('age_detection') or
                self.config.is_enabled('gender_detection')) and self.age_gender_detector:
                result = self.age_gender_detector.analyze_face(frame, face)
                age = result.get('age') if self.config.is_enabled('age_detection') else None
                gender = result.get('gender') if self.config.is_enabled('gender_detection') else None

                if age or gender:
                    self.age_gender_detector.draw_age_gender(
                        display_frame, face, age, gender, self.config.font_scale
                    )
                    if age:
                        face_stats.append(f"Age: {age}")
                    if gender:
                        face_stats.append(f"Gender: {gender}")

            # Emotion
            if self.config.is_enabled('emotion_detection') and self.emotion_detector:
                emotion_result = self.emotion_detector.detect_emotion(frame, face)
                emotion = emotion_result.get('emotion')
                confidence = emotion_result.get('confidence')

                if emotion:
                    self.emotion_detector.draw_emotion(
                        display_frame, face, emotion, confidence, self.config.font_scale
                    )
                    face_stats.append(f"Emotion: {emotion} ({confidence:.0f}%)")

            # Pose
            if self.config.is_enabled('pose_detection') and self.pose_detector:
                pose = self.pose_detector.detect_pose(frame, face)
                if pose:
                    self.pose_detector.draw_pose(
                        display_frame, pose, face, self.config.font_scale
                    )
                    face_stats.append(f"Pose: {pose}")

            # Mask & Glasses
            if self.config.is_enabled('mask_glasses_detection') and self.mask_glasses_detector:
                mg_result = self.mask_glasses_detector.detect(frame, face)
                has_mask = mg_result.get('mask', False)
                has_glasses = mg_result.get('glasses', False)

                if has_mask or has_glasses:
                    self.mask_glasses_detector.draw_attributes(
                        display_frame, face, has_mask, has_glasses, self.config.font_scale - 0.1
                    )

                    attributes = []
                    if has_mask:
                        attributes.append("Mask")
                    if has_glasses:
                        attributes.append("Glasses")
                    face_stats.append(f"Wearing: {', '.join(attributes)}")

            if face_stats:
                stats.append(f"\n**Person {i+1}:** {' | '.join(face_stats)}")

        # Update FPS
        fps = self.fps_monitor.update()
        stats.insert(0, f"⚡ **FPS:** {fps:.1f}")
        stats.insert(1, f"💻 **Device:** {self.device.upper()}")

        # Convert back to RGB for display
        display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)

        return display_frame, "\n".join(stats)

    def process_video(self, video, progress=gr.Progress()):
        """Process video file"""
        if video is None:
            return None, "No video uploaded"

        self.initialize_detectors()

        cap = cv2.VideoCapture(video)
        if not cap.isOpened():
            return None, "Error: Could not open video file"

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Create output video
        output_path = "processed_video.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        stats_summary = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # Update progress
            progress((frame_count / total_frames, f"Processing frame {frame_count}/{total_frames}"))

            # Process frame
            processed_frame, _ = self.process_frame(frame)

            # Convert back to BGR for video writing
            if processed_frame is not None:
                processed_frame_bgr = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)
                out.write(processed_frame_bgr)

        cap.release()
        out.release()

        summary = f"""
## Video Processing Complete!

**Total Frames:** {frame_count}
**Resolution:** {width}x{height}
**FPS:** {fps}
**Output:** {output_path}
        """

        return output_path, summary

    def reset_tracking_db(self):
        """Reset person tracking database"""
        if self.person_tracker:
            self.person_tracker.reset_database()
            return "✓ Person tracking database has been reset"
        return "⚠ Person tracker not initialized"


def create_interface():
    """Create Gradio interface"""
    app = WebCVApp()

    # Custom CSS
    custom_css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .output-image {
        border: 2px solid #4ec9b0;
        border-radius: 8px;
    }
    """

    with gr.Blocks(css=custom_css, title="Computer Vision System", theme=gr.themes.Soft()) as demo:

        gr.Markdown(
            """
            # 🎥 Computer Vision System - Budget Friendly Edition
            ### Multi-Feature Face Analysis with AI

            Upload an image or video, configure features, and let AI analyze it!
            """
        )

        with gr.Tabs():

            # Image Processing Tab
            with gr.Tab("📸 Image Analysis"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### Upload Image")
                        image_input = gr.Image(label="Input Image", type="numpy")

                        gr.Markdown("### ⚙️ Features")

                        face_detection_cb = gr.Checkbox(label="👤 Face Detection", value=True)
                        person_count_cb = gr.Checkbox(label="📊 Person Counting", value=True)
                        unique_tracking_cb = gr.Checkbox(label="🔍 Unique Tracking", value=True)
                        age_detection_cb = gr.Checkbox(label="🎂 Age Detection", value=True)
                        gender_detection_cb = gr.Checkbox(label="⚧️ Gender Detection", value=True)
                        emotion_detection_cb = gr.Checkbox(label="😊 Emotion Detection", value=True)
                        pose_detection_cb = gr.Checkbox(label="🧍 Pose Detection", value=True)
                        mask_glasses_cb = gr.Checkbox(label="😷 Mask & Glasses", value=True)

                        gr.Markdown("### ⚡ Performance")

                        auto_optimize_cb = gr.Checkbox(label="🔄 Auto-Optimize", value=False)
                        target_fps_slider = gr.Slider(
                            minimum=5,
                            maximum=30,
                            value=15,
                            step=1,
                            label="Target FPS"
                        )

                        process_btn = gr.Button("🚀 Process Image", variant="primary", size="lg")
                        reset_btn = gr.Button("🔄 Reset Tracking", variant="secondary")

                    with gr.Column(scale=2):
                        gr.Markdown("### Results")
                        image_output = gr.Image(label="Processed Image", elem_classes=["output-image"])
                        stats_output = gr.Markdown(label="Statistics")

                # Button actions
                process_btn.click(
                    fn=lambda img, fd, pc, ut, ad, gd, ed, pd, mg, ao, tf: (
                        app.update_config(fd, pc, ut, ad, gd, ed, pd, mg, ao, tf),
                        app.process_frame(img)
                    )[1],
                    inputs=[
                        image_input,
                        face_detection_cb,
                        person_count_cb,
                        unique_tracking_cb,
                        age_detection_cb,
                        gender_detection_cb,
                        emotion_detection_cb,
                        pose_detection_cb,
                        mask_glasses_cb,
                        auto_optimize_cb,
                        target_fps_slider
                    ],
                    outputs=[image_output, stats_output]
                )

                reset_btn.click(
                    fn=app.reset_tracking_db,
                    outputs=stats_output
                )

            # Video Processing Tab
            with gr.Tab("🎬 Video Analysis"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Upload Video")
                        video_input = gr.Video(label="Input Video")

                        gr.Markdown("### Settings")
                        video_features_info = gr.Markdown(
                            "Video will be processed with the same feature settings as Image Analysis tab."
                        )

                        process_video_btn = gr.Button("🚀 Process Video", variant="primary", size="lg")

                    with gr.Column():
                        gr.Markdown("### Processed Video")
                        video_output = gr.Video(label="Output Video")
                        video_stats = gr.Markdown(label="Processing Statistics")

                process_video_btn.click(
                    fn=app.process_video,
                    inputs=[video_input],
                    outputs=[video_output, video_stats]
                )

            # Webcam Tab
            with gr.Tab("📹 Live Webcam"):
                gr.Markdown("### Live Processing")
                gr.Markdown("⚠️ Note: This processes frames one at a time. For real-time video, use the desktop GUI application.")

                with gr.Row():
                    webcam_input = gr.Image(label="Webcam", source="webcam", type="numpy")
                    webcam_output = gr.Image(label="Processed", elem_classes=["output-image"])

                webcam_stats = gr.Markdown()

                webcam_input.change(
                    fn=app.process_frame,
                    inputs=[webcam_input],
                    outputs=[webcam_output, webcam_stats]
                )

            # About Tab
            with gr.Tab("ℹ️ About"):
                gr.Markdown(
                    """
                    ## About This System

                    This is a **budget-friendly computer vision system** designed to work on low to high-end hardware.

                    ### Features

                    1. **👤 Face Detection** - Detect and draw bounding boxes around faces
                    2. **📊 Person Counting** - Count number of people in image/video
                    3. **🔍 Unique Tracking** - Track and count unique individuals
                    4. **🎂 Age Detection** - Estimate age of detected persons
                    5. **⚧️ Gender Detection** - Identify gender
                    6. **😊 Emotion Detection** - Detect emotions (happy, sad, angry, etc.)
                    7. **🧍 Pose Detection** - Identify sitting/standing poses
                    8. **😷 Mask & Glasses Detection** - Detect face masks and eyeglasses

                    ### Performance

                    - Auto-detects GPU/CPU and optimizes accordingly
                    - Manual feature toggling for performance control
                    - Auto-optimization mode to maintain target FPS
                    - Works on budget hardware!

                    ### Usage

                    1. Upload an image or video
                    2. Select features you want to enable
                    3. Adjust performance settings if needed
                    4. Click "Process" and view results!

                    ### System Information
                    """
                )

                # Display device info
                device_info = get_device_info()
                device_info_md = f"""
                **Device:** {device_info['device'].upper()}
                **PyTorch CUDA:** {'✓ Available' if device_info['torch_cuda_available'] else '✗ Not Available'}
                **OpenCV CUDA:** {'✓ Available' if device_info['opencv_cuda_available'] else '✗ Not Available'}
                """

                if device_info['torch_cuda_available']:
                    device_info_md += f"""
**GPU:** {device_info.get('gpu_name', 'Unknown')}
**CUDA Version:** {device_info.get('cuda_version', 'Unknown')}
**GPU Memory:** {device_info.get('gpu_memory_total', 0):.2f} GB
                    """

                gr.Markdown(device_info_md)

                gr.Markdown(
                    """
                    ---

                    ### Desktop GUI Available!

                    For real-time video processing, use the desktop GUI:
                    ```bash
                    python gui_app.py
                    ```

                    Or the command-line version:
                    ```bash
                    python main.py --auto-optimize --target-fps 15
                    ```
                    """
                )

        gr.Markdown(
            """
            ---
            <div style="text-align: center; color: #888;">
            Budget-Friendly Computer Vision System | Built with ❤️ using Gradio
            </div>
            """
        )

    return demo


def main():
    """Main entry point for web application"""
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )


if __name__ == '__main__':
    main()
