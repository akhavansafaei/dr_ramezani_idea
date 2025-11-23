"""
Modern GUI Application for Computer Vision System
Professional Tkinter-based interface
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time
from config import Config
from utils.device_utils import detect_device
from utils.fps_monitor import FPSMonitor
from features.face_detector import FaceDetector
from features.person_tracker import PersonTracker
from features.age_gender_detector import AgeGenderDetector
from features.emotion_detector import EmotionDetector
from features.pose_detector import PoseDetector
from features.mask_glasses_detector import MaskGlassesDetector


class ModernCVApp:
    """Modern Computer Vision Application with GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title("Computer Vision System - Budget Friendly Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')

        # State variables
        self.is_running = False
        self.is_paused = False
        self.cap = None
        self.current_frame = None
        self.config = Config()
        self.device = detect_device()

        # Feature detectors (initialized on start)
        self.face_detector = None
        self.person_tracker = None
        self.age_gender_detector = None
        self.emotion_detector = None
        self.pose_detector = None
        self.mask_glasses_detector = None
        self.fps_monitor = None

        # Statistics
        self.stats = {
            'fps': 0,
            'people_count': 0,
            'unique_count': 0,
            'device': self.device
        }

        # Setup UI
        self.setup_ui()

        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        """Setup the user interface"""

        # Main container
        main_container = tk.Frame(self.root, bg='#1e1e1e')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Panel - Controls
        self.setup_left_panel(main_container)

        # Right Panel - Video and Stats
        self.setup_right_panel(main_container)

    def setup_left_panel(self, parent):
        """Setup left control panel"""
        left_panel = tk.Frame(parent, bg='#252526', relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.configure(width=350)

        # Title
        title_label = tk.Label(
            left_panel,
            text="⚙️ Control Panel",
            font=('Segoe UI', 16, 'bold'),
            bg='#252526',
            fg='#ffffff'
        )
        title_label.pack(pady=(15, 20))

        # Source Selection
        self.setup_source_section(left_panel)

        # Separator
        ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=15)

        # Feature Controls
        self.setup_feature_section(left_panel)

        # Separator
        ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=15)

        # Performance Settings
        self.setup_performance_section(left_panel)

        # Separator
        ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=15)

        # Action Buttons
        self.setup_action_buttons(left_panel)

    def setup_source_section(self, parent):
        """Setup source selection section"""
        section_frame = tk.Frame(parent, bg='#252526')
        section_frame.pack(fill=tk.X, padx=15)

        tk.Label(
            section_frame,
            text="📹 Video Source",
            font=('Segoe UI', 11, 'bold'),
            bg='#252526',
            fg='#4ec9b0'
        ).pack(anchor=tk.W, pady=(0, 8))

        # Source type
        source_type_frame = tk.Frame(section_frame, bg='#252526')
        source_type_frame.pack(fill=tk.X, pady=5)

        self.source_var = tk.StringVar(value="webcam")

        tk.Radiobutton(
            source_type_frame,
            text="Webcam",
            variable=self.source_var,
            value="webcam",
            bg='#252526',
            fg='#ffffff',
            selectcolor='#3c3c3c',
            activebackground='#252526',
            activeforeground='#ffffff',
            font=('Segoe UI', 9)
        ).pack(anchor=tk.W)

        tk.Radiobutton(
            source_type_frame,
            text="Video File",
            variable=self.source_var,
            value="file",
            bg='#252526',
            fg='#ffffff',
            selectcolor='#3c3c3c',
            activebackground='#252526',
            activeforeground='#ffffff',
            font=('Segoe UI', 9)
        ).pack(anchor=tk.W)

        # File selection
        file_frame = tk.Frame(section_frame, bg='#252526')
        file_frame.pack(fill=tk.X, pady=5)

        self.file_path_var = tk.StringVar(value="")

        tk.Button(
            file_frame,
            text="Browse...",
            command=self.browse_file,
            bg='#3c3c3c',
            fg='#ffffff',
            relief=tk.FLAT,
            padx=10,
            font=('Segoe UI', 9)
        ).pack(side=tk.LEFT)

        self.file_label = tk.Label(
            file_frame,
            textvariable=self.file_path_var,
            bg='#252526',
            fg='#888888',
            font=('Segoe UI', 8)
        )
        self.file_label.pack(side=tk.LEFT, padx=10)

    def setup_feature_section(self, parent):
        """Setup feature toggles section"""
        section_frame = tk.Frame(parent, bg='#252526')
        section_frame.pack(fill=tk.X, padx=15)

        tk.Label(
            section_frame,
            text="✨ Features",
            font=('Segoe UI', 11, 'bold'),
            bg='#252526',
            fg='#4ec9b0'
        ).pack(anchor=tk.W, pady=(0, 8))

        # Create checkboxes for each feature
        self.feature_vars = {}

        features_display = {
            'face_detection': '👤 Face Detection',
            'person_count': '📊 Person Counting',
            'unique_tracking': '🔍 Unique Tracking',
            'age_detection': '🎂 Age Detection',
            'gender_detection': '⚧️ Gender Detection',
            'emotion_detection': '😊 Emotion Detection',
            'pose_detection': '🧍 Pose Detection',
            'mask_glasses_detection': '😷 Mask & Glasses'
        }

        for feature_key, feature_label in features_display.items():
            var = tk.BooleanVar(value=self.config.is_enabled(feature_key))
            self.feature_vars[feature_key] = var

            cb = tk.Checkbutton(
                section_frame,
                text=feature_label,
                variable=var,
                bg='#252526',
                fg='#ffffff',
                selectcolor='#3c3c3c',
                activebackground='#252526',
                activeforeground='#ffffff',
                font=('Segoe UI', 9),
                command=lambda k=feature_key: self.toggle_feature(k)
            )
            cb.pack(anchor=tk.W, pady=2)

    def setup_performance_section(self, parent):
        """Setup performance settings section"""
        section_frame = tk.Frame(parent, bg='#252526')
        section_frame.pack(fill=tk.X, padx=15)

        tk.Label(
            section_frame,
            text="⚡ Performance",
            font=('Segoe UI', 11, 'bold'),
            bg='#252526',
            fg='#4ec9b0'
        ).pack(anchor=tk.W, pady=(0, 8))

        # Auto-optimize toggle
        self.auto_optimize_var = tk.BooleanVar(value=self.config.auto_optimize)
        tk.Checkbutton(
            section_frame,
            text="🔄 Auto-Optimize",
            variable=self.auto_optimize_var,
            bg='#252526',
            fg='#ffffff',
            selectcolor='#3c3c3c',
            activebackground='#252526',
            activeforeground='#ffffff',
            font=('Segoe UI', 9),
            command=self.toggle_auto_optimize
        ).pack(anchor=tk.W, pady=2)

        # Target FPS
        fps_frame = tk.Frame(section_frame, bg='#252526')
        fps_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            fps_frame,
            text="Target FPS:",
            bg='#252526',
            fg='#ffffff',
            font=('Segoe UI', 9)
        ).pack(side=tk.LEFT)

        self.fps_value_label = tk.Label(
            fps_frame,
            text=str(self.config.target_fps),
            bg='#252526',
            fg='#4ec9b0',
            font=('Segoe UI', 9, 'bold')
        )
        self.fps_value_label.pack(side=tk.RIGHT)

        self.fps_scale = tk.Scale(
            section_frame,
            from_=5,
            to=30,
            orient=tk.HORIZONTAL,
            bg='#252526',
            fg='#ffffff',
            troughcolor='#3c3c3c',
            highlightthickness=0,
            command=self.update_target_fps
        )
        self.fps_scale.set(self.config.target_fps)
        self.fps_scale.pack(fill=tk.X)

        # Device selection
        device_frame = tk.Frame(section_frame, bg='#252526')
        device_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            device_frame,
            text="Device:",
            bg='#252526',
            fg='#ffffff',
            font=('Segoe UI', 9)
        ).pack(side=tk.LEFT)

        self.device_label = tk.Label(
            device_frame,
            text=self.device.upper(),
            bg='#252526',
            fg='#ffd700' if self.device == 'cuda' else '#888888',
            font=('Segoe UI', 9, 'bold')
        )
        self.device_label.pack(side=tk.RIGHT)

    def setup_action_buttons(self, parent):
        """Setup action buttons section"""
        section_frame = tk.Frame(parent, bg='#252526')
        section_frame.pack(fill=tk.X, padx=15, pady=10)

        # Start button
        self.start_button = tk.Button(
            section_frame,
            text="▶️ Start",
            command=self.start_processing,
            bg='#0e7a0d',
            fg='#ffffff',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            font=('Segoe UI', 11, 'bold'),
            cursor='hand2'
        )
        self.start_button.pack(fill=tk.X, pady=5)

        # Pause button
        self.pause_button = tk.Button(
            section_frame,
            text="⏸️ Pause",
            command=self.pause_processing,
            bg='#f59700',
            fg='#ffffff',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            font=('Segoe UI', 11, 'bold'),
            cursor='hand2',
            state=tk.DISABLED
        )
        self.pause_button.pack(fill=tk.X, pady=5)

        # Stop button
        self.stop_button = tk.Button(
            section_frame,
            text="⏹️ Stop",
            command=self.stop_processing,
            bg='#a80000',
            fg='#ffffff',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            font=('Segoe UI', 11, 'bold'),
            cursor='hand2',
            state=tk.DISABLED
        )
        self.stop_button.pack(fill=tk.X, pady=5)

        # Utility buttons
        util_frame = tk.Frame(section_frame, bg='#252526')
        util_frame.pack(fill=tk.X, pady=15)

        tk.Button(
            util_frame,
            text="📸 Screenshot",
            command=self.take_screenshot,
            bg='#3c3c3c',
            fg='#ffffff',
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=('Segoe UI', 9)
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        tk.Button(
            util_frame,
            text="🔄 Reset",
            command=self.reset_tracking,
            bg='#3c3c3c',
            fg='#ffffff',
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=('Segoe UI', 9)
        ).pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=2)

    def setup_right_panel(self, parent):
        """Setup right panel with video and stats"""
        right_panel = tk.Frame(parent, bg='#1e1e1e')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Stats Panel (top)
        self.setup_stats_panel(right_panel)

        # Video Display (center)
        self.setup_video_display(right_panel)

        # Status Bar (bottom)
        self.setup_status_bar(right_panel)

    def setup_stats_panel(self, parent):
        """Setup statistics panel"""
        stats_panel = tk.Frame(parent, bg='#252526', relief=tk.RAISED, bd=2)
        stats_panel.pack(fill=tk.X, pady=(0, 10))

        # Title
        tk.Label(
            stats_panel,
            text="📊 Real-time Statistics",
            font=('Segoe UI', 12, 'bold'),
            bg='#252526',
            fg='#ffffff'
        ).pack(pady=10)

        # Stats grid
        stats_grid = tk.Frame(stats_panel, bg='#252526')
        stats_grid.pack(fill=tk.X, padx=20, pady=(0, 15))

        # Create stat boxes
        self.stat_labels = {}

        stats_info = [
            ('fps', '⚡ FPS', '0.0', '#4ec9b0'),
            ('people', '👥 People', '0', '#569cd6'),
            ('unique', '🔍 Unique', '0', '#dcdcaa'),
            ('device', '💻 Device', self.device.upper(), '#ffd700' if self.device == 'cuda' else '#888888')
        ]

        for i, (key, label, default, color) in enumerate(stats_info):
            stat_box = tk.Frame(stats_grid, bg='#1e1e1e', relief=tk.RAISED, bd=1)
            stat_box.grid(row=0, column=i, padx=10, pady=5, sticky='ew')
            stats_grid.columnconfigure(i, weight=1)

            tk.Label(
                stat_box,
                text=label,
                bg='#1e1e1e',
                fg='#888888',
                font=('Segoe UI', 9)
            ).pack(pady=(8, 2))

            value_label = tk.Label(
                stat_box,
                text=default,
                bg='#1e1e1e',
                fg=color,
                font=('Segoe UI', 18, 'bold')
            )
            value_label.pack(pady=(2, 8))

            self.stat_labels[key] = value_label

    def setup_video_display(self, parent):
        """Setup video display area"""
        video_frame = tk.Frame(parent, bg='#000000', relief=tk.SUNKEN, bd=2)
        video_frame.pack(fill=tk.BOTH, expand=True)

        # Video label
        self.video_label = tk.Label(video_frame, bg='#000000')
        self.video_label.pack(fill=tk.BOTH, expand=True)

        # Placeholder text
        self.placeholder_label = tk.Label(
            video_frame,
            text="🎥\n\nNo Video Feed\n\nClick 'Start' to begin",
            font=('Segoe UI', 20),
            bg='#000000',
            fg='#888888'
        )
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def setup_status_bar(self, parent):
        """Setup status bar"""
        status_bar = tk.Frame(parent, bg='#007acc', relief=tk.FLAT, bd=0)
        status_bar.pack(fill=tk.X, pady=(10, 0))

        self.status_label = tk.Label(
            status_bar,
            text="Ready",
            bg='#007acc',
            fg='#ffffff',
            font=('Segoe UI', 9),
            anchor=tk.W,
            padx=10,
            pady=5
        )
        self.status_label.pack(fill=tk.X)

    # Event Handlers
    def browse_file(self):
        """Browse for video file"""
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.file_path_var.set(filename[:30] + "..." if len(filename) > 30 else filename)
            self.source_var.set("file")

    def toggle_feature(self, feature_key):
        """Toggle feature on/off"""
        if self.feature_vars[feature_key].get():
            self.config.enable_feature(feature_key)
        else:
            self.config.disable_feature(feature_key)

    def toggle_auto_optimize(self):
        """Toggle auto-optimization"""
        self.config.auto_optimize = self.auto_optimize_var.get()

    def update_target_fps(self, value):
        """Update target FPS"""
        fps = int(float(value))
        self.config.target_fps = fps
        self.fps_value_label.config(text=str(fps))

    def start_processing(self):
        """Start video processing"""
        if self.is_running:
            return

        # Get source
        if self.source_var.get() == "webcam":
            source = 0
        else:
            source = self.file_path_var.get()
            if not source:
                messagebox.showerror("Error", "Please select a video file")
                return

        # Initialize capture
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            messagebox.showerror("Error", f"Could not open video source: {source}")
            return

        # Initialize detectors
        self.initialize_detectors()

        # Update UI
        self.is_running = True
        self.is_paused = False
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        self.placeholder_label.place_forget()
        self.update_status("Processing...")

        # Start processing thread
        self.processing_thread = threading.Thread(target=self.process_video, daemon=True)
        self.processing_thread.start()

    def pause_processing(self):
        """Pause/Resume video processing"""
        if not self.is_running:
            return

        self.is_paused = not self.is_paused

        if self.is_paused:
            self.pause_button.config(text="▶️ Resume")
            self.update_status("Paused")
        else:
            self.pause_button.config(text="⏸️ Pause")
            self.update_status("Processing...")

    def stop_processing(self):
        """Stop video processing"""
        if not self.is_running:
            return

        self.is_running = False
        self.is_paused = False

        if self.cap:
            self.cap.release()
            self.cap = None

        # Update UI
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED, text="⏸️ Pause")
        self.stop_button.config(state=tk.DISABLED)
        self.video_label.config(image='')
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.update_status("Stopped")

    def take_screenshot(self):
        """Take screenshot of current frame"""
        if self.current_frame is not None:
            filename = f"screenshot_{int(time.time())}.jpg"
            cv2.imwrite(filename, self.current_frame)
            self.update_status(f"Screenshot saved: {filename}")
            messagebox.showinfo("Success", f"Screenshot saved as:\n{filename}")

    def reset_tracking(self):
        """Reset person tracking database"""
        if self.person_tracker:
            self.person_tracker.reset_database()
            self.update_status("Person tracking database reset")
            messagebox.showinfo("Success", "Person tracking database has been reset")

    def initialize_detectors(self):
        """Initialize all feature detectors"""
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

    def process_video(self):
        """Main video processing loop"""
        frame_count = 0

        while self.is_running:
            if self.is_paused:
                time.sleep(0.1)
                continue

            ret, frame = self.cap.read()
            if not ret:
                self.root.after(0, self.stop_processing)
                break

            frame_count += 1

            # Resize for performance
            if self.config.resize_width:
                height, width = frame.shape[:2]
                if width > self.config.resize_width:
                    scale = self.config.resize_width / width
                    frame = cv2.resize(frame, None, fx=scale, fy=scale)

            # Process frame
            processed_frame = self.process_frame(frame)
            self.current_frame = processed_frame

            # Update FPS
            fps = self.fps_monitor.update()
            self.stats['fps'] = fps

            # Auto-optimize
            if frame_count % 30 == 0 and self.config.auto_optimize:
                self.auto_optimize()

            # Update display
            self.root.after(0, self.update_video_display, processed_frame)
            self.root.after(0, self.update_stats_display)

    def process_frame(self, frame):
        """Process a single frame"""
        display_frame = frame.copy()

        # Face detection
        faces = []
        if self.config.is_enabled('face_detection'):
            faces = self.face_detector.detect_faces(frame)
            for face in faces:
                x, y, w, h = face
                cv2.rectangle(display_frame, (x, y), (x + w, y + h),
                            (0, 255, 0), self.config.box_thickness)

        # Update stats
        self.stats['people_count'] = len(faces)

        # Unique tracking
        if self.config.is_enabled('unique_tracking') and self.person_tracker and len(faces) > 0:
            for face in faces:
                self.person_tracker.identify_or_register_face(frame, face)
            self.stats['unique_count'] = self.person_tracker.get_unique_count()

        # Process each face
        for face in faces:
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

            # Emotion
            if self.config.is_enabled('emotion_detection') and self.emotion_detector:
                emotion_result = self.emotion_detector.detect_emotion(frame, face)
                emotion = emotion_result.get('emotion')
                confidence = emotion_result.get('confidence')
                if emotion:
                    self.emotion_detector.draw_emotion(
                        display_frame, face, emotion, confidence, self.config.font_scale
                    )

            # Pose
            if self.config.is_enabled('pose_detection') and self.pose_detector:
                pose = self.pose_detector.detect_pose(frame, face)
                if pose:
                    self.pose_detector.draw_pose(
                        display_frame, pose, face, self.config.font_scale
                    )

            # Mask & Glasses
            if self.config.is_enabled('mask_glasses_detection') and self.mask_glasses_detector:
                mg_result = self.mask_glasses_detector.detect(frame, face)
                has_mask = mg_result.get('mask', False)
                has_glasses = mg_result.get('glasses', False)
                if has_mask or has_glasses:
                    self.mask_glasses_detector.draw_attributes(
                        display_frame, face, has_mask, has_glasses, self.config.font_scale - 0.1
                    )

        return display_frame

    def auto_optimize(self):
        """Auto-optimize performance"""
        if not self.config.auto_optimize:
            return

        if self.fps_monitor.should_disable_feature():
            disabled = self.config.disable_lowest_priority_feature()
            if disabled:
                self.root.after(0, lambda: self.feature_vars[disabled].set(False))
                self.fps_monitor.reset()
                self.update_status(f"Auto-disabled: {self.config.features[disabled]['name']}")

        elif self.fps_monitor.should_enable_feature():
            enabled = self.config.enable_highest_priority_disabled_feature()
            if enabled:
                self.root.after(0, lambda: self.feature_vars[enabled].set(True))
                self.fps_monitor.reset()
                self.update_status(f"Auto-enabled: {self.config.features[enabled]['name']}")

    def update_video_display(self, frame):
        """Update video display"""
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to PIL Image
        img = Image.fromarray(frame_rgb)

        # Resize to fit display
        display_width = self.video_label.winfo_width()
        display_height = self.video_label.winfo_height()

        if display_width > 1 and display_height > 1:
            img.thumbnail((display_width, display_height), Image.Resampling.LANCZOS)

        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(img)

        # Update label
        self.video_label.config(image=photo)
        self.video_label.image = photo

    def update_stats_display(self):
        """Update statistics display"""
        self.stat_labels['fps'].config(text=f"{self.stats['fps']:.1f}")
        self.stat_labels['people'].config(text=str(self.stats['people_count']))
        self.stat_labels['unique'].config(text=str(self.stats['unique_count']))

    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)

    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Processing is running. Do you want to quit?"):
                self.is_running = False
                if self.cap:
                    self.cap.release()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Main entry point for GUI application"""
    root = tk.Tk()
    app = ModernCVApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
