"""
FPS Monitoring and Auto-optimization
"""
import time
from collections import deque


class FPSMonitor:
    """Monitor FPS and trigger auto-optimization"""

    def __init__(self, target_fps=15, window_size=30):
        self.target_fps = target_fps
        self.window_size = window_size
        self.frame_times = deque(maxlen=window_size)
        self.last_time = time.time()
        self.current_fps = 0

    def update(self):
        """Update FPS calculation"""
        current_time = time.time()
        delta = current_time - self.last_time
        self.last_time = current_time

        if delta > 0:
            self.frame_times.append(delta)

        # Calculate average FPS
        if len(self.frame_times) > 0:
            avg_time = sum(self.frame_times) / len(self.frame_times)
            self.current_fps = 1.0 / avg_time if avg_time > 0 else 0

        return self.current_fps

    def get_fps(self):
        """Get current FPS"""
        return self.current_fps

    def should_disable_feature(self):
        """Check if we should disable a feature to improve FPS"""
        # Only suggest disabling if we have enough samples
        if len(self.frame_times) < self.window_size * 0.7:
            return False

        # Disable if FPS is below target
        return self.current_fps < self.target_fps * 0.9  # 10% tolerance

    def should_enable_feature(self):
        """Check if we can enable a feature (FPS is good)"""
        # Only suggest enabling if we have enough samples
        if len(self.frame_times) < self.window_size * 0.7:
            return False

        # Enable if FPS is well above target
        return self.current_fps > self.target_fps * 1.2  # 20% headroom

    def reset(self):
        """Reset FPS monitoring"""
        self.frame_times.clear()
        self.last_time = time.time()
