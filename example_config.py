"""
Example Configuration Script
Shows how to customize the system for different scenarios
"""

from config import Config


def get_low_end_config():
    """Configuration optimized for low-end systems"""
    config = Config()

    # Use fastest methods
    config.face_detection_method = 'opencv'
    config.resize_width = 480
    config.frame_skip = 2  # Process every other frame

    # Disable heavy features
    config.disable_feature('emotion_detection')
    config.disable_feature('pose_detection')
    config.disable_feature('age_detection')

    # Enable auto-optimization
    config.auto_optimize = True
    config.target_fps = 10

    return config


def get_mid_range_config():
    """Configuration for mid-range systems"""
    config = Config()

    # Balanced settings
    config.face_detection_method = 'opencv'
    config.resize_width = 640
    config.frame_skip = 1

    # Keep most features, disable pose
    config.disable_feature('pose_detection')

    # Enable auto-optimization with higher target
    config.auto_optimize = True
    config.target_fps = 15

    return config


def get_high_end_config():
    """Configuration for high-end systems with GPU"""
    config = Config()

    # Best quality
    config.face_detection_method = 'retinaface'
    config.resize_width = 1280
    config.frame_skip = 1

    # All features enabled (default)
    # No auto-optimization needed
    config.auto_optimize = False
    config.target_fps = 30

    return config


def get_emotion_only_config():
    """Configuration focused on emotion detection"""
    config = Config()

    # Keep only face detection and emotion
    config.disable_feature('unique_tracking')
    config.disable_feature('age_detection')
    config.disable_feature('gender_detection')
    config.disable_feature('pose_detection')
    config.disable_feature('mask_glasses_detection')

    config.auto_optimize = True
    config.target_fps = 20

    return config


def get_tracking_only_config():
    """Configuration focused on person tracking"""
    config = Config()

    # Keep only face detection, counting, and tracking
    config.disable_feature('age_detection')
    config.disable_feature('gender_detection')
    config.disable_feature('emotion_detection')
    config.disable_feature('pose_detection')
    config.disable_feature('mask_glasses_detection')

    config.auto_optimize = True
    config.target_fps = 20

    return config


# Example usage:
if __name__ == '__main__':
    print("Example Configurations:")
    print("=" * 60)

    configs = {
        "Low-End System": get_low_end_config(),
        "Mid-Range System": get_mid_range_config(),
        "High-End System": get_high_end_config(),
        "Emotion Detection Focus": get_emotion_only_config(),
        "Person Tracking Focus": get_tracking_only_config(),
    }

    for name, config in configs.items():
        print(f"\n{name}:")
        print(f"  Detection Method: {config.face_detection_method}")
        print(f"  Resolution: {config.resize_width}px")
        print(f"  Target FPS: {config.target_fps}")
        print(f"  Auto-Optimize: {config.auto_optimize}")
        print(f"  Enabled Features:")
        for feature_name, feature_info in config.features.items():
            if feature_info['enabled']:
                print(f"    - {feature_info['name']}")
