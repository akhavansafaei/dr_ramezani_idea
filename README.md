# Budget-Friendly Computer Vision System 🎥👁️

A comprehensive, hardware-aware computer vision system designed for low to mid-range systems. Features automatic GPU/CPU detection and intelligent performance optimization.

## ✨ Features

### Core Capabilities
1. **Face Detection** - Draw bounding boxes around detected faces
2. **Person Counting** - Real-time count of people in frame
3. **Unique Person Tracking** - Identify and count unique individuals
4. **Age Detection** - Estimate age of detected persons
5. **Gender Detection** - Identify gender
6. **Emotion Detection** - Detect emotions (happy, sad, angry, surprise, fear, disgust, neutral)
7. **Pose Detection** - Identify sitting/standing poses
8. **Mask & Glasses Detection** - Detect face masks and eyeglasses

### System Features
- ✅ **Auto GPU/CPU Detection** - Automatically uses best available hardware
- ✅ **Manual Feature Toggle** - Enable/disable features individually
- ✅ **Auto-Optimization** - Automatically disable features to maintain target FPS
- ✅ **Priority-Based** - Features disabled in order of priority when optimizing
- ✅ **Real-time FPS Monitoring** - See performance metrics live
- ✅ **Face Database** - Save and track unique individuals across sessions

## 📋 Requirements

### System Requirements

**Minimum:**
- CPU: Dual-core processor
- RAM: 4GB
- OS: Windows, Linux, or macOS
- Python: 3.8+

**Recommended:**
- CPU: Quad-core processor or better
- RAM: 8GB+
- GPU: NVIDIA GPU with CUDA support (optional, but recommended)
- Python: 3.9+

### Software Dependencies

See `requirements.txt` for full list. Main dependencies:
- OpenCV
- PyTorch
- DeepFace
- MediaPipe (optional, for better pose detection)
- NumPy

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd dr_ramezani_idea
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Install CUDA Support
If you have an NVIDIA GPU, install CUDA-enabled PyTorch:
```bash
# Visit https://pytorch.org/ for specific installation command
# Example for CUDA 11.8:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## 💻 Usage

### Basic Usage (Webcam)
```bash
python main.py
```

### Use Video File
```bash
python main.py --source path/to/video.mp4
```

### Enable Auto-Optimization
```bash
# System will automatically disable features to maintain 15 FPS
python main.py --auto-optimize --target-fps 15
```

### Force CPU Mode
```bash
python main.py --device cpu
```

### Disable Specific Features
```bash
# Disable age and emotion detection for better performance
python main.py --disable age_detection emotion_detection
```

### Full Example
```bash
python main.py \
    --source 0 \
    --auto-optimize \
    --target-fps 20 \
    --device auto \
    --disable pose_detection
```

## ⚙️ Configuration

Edit `config.py` to customize:

### Feature Priority
Features are disabled in this order (when auto-optimizing):
1. Face Detection (highest priority - never disabled)
2. Person Counting
3. Unique Tracking
4. Age Detection
5. Gender Detection
6. Emotion Detection
7. Pose Detection
8. Mask & Glasses Detection (lowest priority - disabled first)

### Performance Settings
```python
# In config.py
self.target_fps = 15              # Target FPS
self.resize_width = 640           # Resize input for performance
self.frame_skip = 1               # Process every Nth frame
```

### Face Detection Method
```python
self.face_detection_method = 'opencv'  # Options: 'opencv', 'mtcnn', 'mediapipe', 'retinaface'
```

## 🎮 Keyboard Controls

While the application is running:
- **Q** - Quit application
- **S** - Save screenshot
- **R** - Reset person tracking database

## 📊 Performance Tips

### For Low-End Systems
1. Enable auto-optimization:
   ```bash
   python main.py --auto-optimize --target-fps 10
   ```

2. Disable heavy features manually:
   ```bash
   python main.py --disable emotion_detection pose_detection age_detection
   ```

3. Use faster face detection:
   ```python
   # In config.py
   self.face_detection_method = 'opencv'  # Fastest
   ```

4. Reduce input resolution:
   ```python
   # In config.py
   self.resize_width = 480  # Lower resolution
   ```

### For Mid-Range Systems
1. Use auto-optimization with higher target:
   ```bash
   python main.py --auto-optimize --target-fps 20
   ```

2. Keep most features enabled
3. Use MediaPipe for face detection (good balance)

### For High-End Systems (with GPU)
1. Enable all features:
   ```bash
   python main.py --target-fps 30
   ```

2. Use RetinaFace for better accuracy:
   ```python
   # In config.py
   self.face_detection_method = 'retinaface'
   ```

## 📁 Project Structure

```
dr_ramezani_idea/
├── main.py                          # Main application
├── config.py                        # Configuration
├── requirements.txt                 # Dependencies
├── README.md                        # This file
├── utils/
│   ├── __init__.py
│   ├── device_utils.py             # GPU/CPU detection
│   └── fps_monitor.py              # FPS monitoring
├── features/
│   ├── __init__.py
│   ├── face_detector.py            # Face detection
│   ├── person_tracker.py           # Unique person tracking
│   ├── age_gender_detector.py     # Age & gender
│   ├── emotion_detector.py         # Emotion detection
│   ├── pose_detector.py            # Pose detection
│   └── mask_glasses_detector.py   # Mask & glasses
└── face_database/                   # Saved faces (auto-created)
```

## 🔧 Troubleshooting

### "No GPU detected" but I have NVIDIA GPU
- Install CUDA-enabled PyTorch (see installation section)
- Check NVIDIA drivers are installed: `nvidia-smi`

### Low FPS
- Enable auto-optimization: `--auto-optimize`
- Reduce target resolution in `config.py`
- Disable non-essential features
- Use OpenCV face detection (fastest)

### "Module not found" errors
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

### Webcam not working
- Check camera permissions
- Try different source number: `--source 1` or `--source 2`
- On Linux, you may need to add user to video group

### Face detection not accurate
- Try different detection methods in `config.py`
- Improve lighting conditions
- Reduce distance from camera

## 🌐 Language Support

The system supports Persian (Farsi) and English. All features work with both languages:
- ترسیم مربع بین چهره افراد ✅
- نمایش تعداد افراد در تصویر ✅
- ذخیره چهره افراد و شمارش افراد یکتا ✅
- تشخیص سن افراد ✅
- تشخیص جنسیت افراد ✅
- تشخیص حالت خنده، غم و ... افراد ✅
- تشخیص حالت نشسته / ایستاده افراد ✅
- تشخیص ماسک زده / عینک زده ✅

## 📝 License

This project is provided as-is for educational and research purposes.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📧 Support

For questions or issues, please create an issue in the repository.

---

**Built for budget-friendly systems with performance in mind! 🚀**
