"""
Configuration file for Computer Vision Project
Manages feature toggles and system settings
"""

class Config:
    """Configuration class for managing CV features and system settings"""

    def __init__(self):
        # System settings
        self.device = 'auto'  # 'auto', 'cpu', or 'cuda'
        self.target_fps = 15  # Target FPS for auto-optimization
        self.auto_optimize = False  # Auto-disable features to maintain FPS

        # Feature toggles (priority order - lower number = higher priority)
        self.features = {
            'face_detection': {
                'enabled': True,
                'priority': 1,
                'name': 'Face Detection & Bounding Boxes'
            },
            'person_count': {
                'enabled': True,
                'priority': 2,
                'name': 'Person Counting'
            },
            'unique_tracking': {
                'enabled': True,
                'priority': 3,
                'name': 'Unique Person Tracking'
            },
            'age_detection': {
                'enabled': True,
                'priority': 4,
                'name': 'Age Detection'
            },
            'gender_detection': {
                'enabled': True,
                'priority': 5,
                'name': 'Gender Detection'
            },
            'emotion_detection': {
                'enabled': True,
                'priority': 6,
                'name': 'Emotion Detection'
            },
            'pose_detection': {
                'enabled': True,
                'priority': 7,
                'name': 'Pose Detection (Sitting/Standing)'
            },
            'mask_glasses_detection': {
                'enabled': True,
                'priority': 8,
                'name': 'Mask & Glasses Detection'
            }
        }

        # Face detection settings
        self.face_detection_confidence = 0.5
        self.face_detection_method = 'opencv'  # 'opencv', 'mtcnn', 'retinaface', 'mediapipe'

        # Face recognition settings (for unique tracking)
        self.face_similarity_threshold = 0.6
        self.face_database_path = 'face_database'

        # Display settings
        self.show_fps = True
        self.show_device = True
        self.font_scale = 0.6
        self.box_thickness = 2

        # Performance settings
        self.frame_skip = 1  # Process every Nth frame
        self.resize_width = 640  # Resize input for faster processing

    def enable_feature(self, feature_name):
        """Enable a specific feature"""
        if feature_name in self.features:
            self.features[feature_name]['enabled'] = True

    def disable_feature(self, feature_name):
        """Disable a specific feature"""
        if feature_name in self.features:
            self.features[feature_name]['enabled'] = False

    def is_enabled(self, feature_name):
        """Check if a feature is enabled"""
        return self.features.get(feature_name, {}).get('enabled', False)

    def get_enabled_features(self):
        """Get list of enabled features sorted by priority"""
        enabled = [(k, v) for k, v in self.features.items() if v['enabled']]
        return sorted(enabled, key=lambda x: x[1]['priority'])

    def get_disabled_features(self):
        """Get list of disabled features sorted by priority (reverse)"""
        disabled = [(k, v) for k, v in self.features.items() if not v['enabled']]
        return sorted(disabled, key=lambda x: x[1]['priority'], reverse=True)

    def disable_lowest_priority_feature(self):
        """Disable the lowest priority enabled feature"""
        enabled = self.get_enabled_features()
        if enabled:
            # Get lowest priority (highest priority number)
            feature_to_disable = enabled[-1][0]
            self.disable_feature(feature_to_disable)
            return feature_to_disable
        return None

    def enable_highest_priority_disabled_feature(self):
        """Enable the highest priority disabled feature"""
        disabled = self.get_disabled_features()
        if disabled:
            # Get highest priority (lowest priority number)
            feature_to_enable = disabled[-1][0]
            self.enable_feature(feature_to_enable)
            return feature_to_enable
        return None
