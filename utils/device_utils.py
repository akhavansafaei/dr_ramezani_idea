"""
Device detection and management utilities
"""
import torch
import cv2


def detect_device():
    """
    Automatically detect the best available device (GPU/CPU)
    Returns: 'cuda' if GPU available, 'cpu' otherwise
    """
    if torch.cuda.is_available():
        device = 'cuda'
        gpu_name = torch.cuda.get_device_name(0)
        print(f"✓ GPU detected: {gpu_name}")
        print(f"  CUDA version: {torch.version.cuda}")
    else:
        device = 'cpu'
        print("✓ Using CPU (No GPU detected)")

    # Check OpenCV CUDA support
    if cv2.cuda.getCudaEnabledDeviceCount() > 0:
        print(f"✓ OpenCV CUDA support: Available")
    else:
        print(f"  OpenCV CUDA support: Not available")

    return device


def get_device_info():
    """Get detailed device information"""
    info = {
        'torch_cuda_available': torch.cuda.is_available(),
        'opencv_cuda_available': cv2.cuda.getCudaEnabledDeviceCount() > 0,
        'device': 'cuda' if torch.cuda.is_available() else 'cpu'
    }

    if info['torch_cuda_available']:
        info['gpu_name'] = torch.cuda.get_device_name(0)
        info['cuda_version'] = torch.version.cuda
        info['gpu_memory_total'] = torch.cuda.get_device_properties(0).total_memory / 1024**3  # GB
        info['gpu_memory_allocated'] = torch.cuda.memory_allocated(0) / 1024**3  # GB

    return info
