# Quick Start Guide 🚀

Get up and running in 5 minutes!

## Step 1: Install Dependencies ⚙️

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

## Step 2: Run the System 🎬

### Default (Webcam, All Features)
```bash
python main.py
```

### With Auto-Optimization (Recommended for Budget Systems)
```bash
python main.py --auto-optimize --target-fps 15
```

### Using a Video File
```bash
python main.py --source path/to/your/video.mp4
```

## Step 3: Interact with the System 🎮

- **Press 'Q'** to quit
- **Press 'S'** to save screenshot
- **Press 'R'** to reset person tracking

## Common Scenarios 📖

### 1. Low-End System (Laptop, Old PC)
```bash
python main.py --auto-optimize --target-fps 10 --disable emotion_detection pose_detection
```

### 2. Mid-Range System (Desktop, Modern Laptop)
```bash
python main.py --auto-optimize --target-fps 20
```

### 3. High-End System (Gaming PC with GPU)
```bash
python main.py --target-fps 30
```

### 4. Only Track People (Fastest)
```bash
python main.py --disable age_detection gender_detection emotion_detection pose_detection mask_glasses_detection
```

### 5. Focus on Emotions
```bash
python main.py --disable pose_detection unique_tracking age_detection mask_glasses_detection
```

## Customizing Features 🔧

Edit `config.py` to change:
- Face detection method (opencv, mtcnn, mediapipe, retinaface)
- Target FPS
- Video resolution
- Feature priorities
- And more!

Or use one of the example configs:
```python
from example_config import get_low_end_config
config = get_low_end_config()
# Use this config in your code
```

## Troubleshooting 🔍

### Problem: Low FPS
**Solution:** Enable auto-optimization and lower target FPS
```bash
python main.py --auto-optimize --target-fps 10
```

### Problem: No webcam detected
**Solution:** Try different camera index
```bash
python main.py --source 1  # or --source 2
```

### Problem: High CPU usage
**Solution:** Reduce resolution and disable heavy features
```python
# In config.py
self.resize_width = 480
self.frame_skip = 2
```

## What's Happening? 📊

The system displays:
- **Green boxes** around faces
- **FPS** in top-left (current performance)
- **Device** (CPU or CUDA/GPU)
- **People count** (current number in frame)
- **Unique count** (total unique people seen)
- **Age, Gender, Emotion** labels near faces
- **Pose** (sitting/standing) if detected
- **Mask/Glasses** indicators

## Next Steps 📚

1. Read the full [README.md](README.md) for detailed documentation
2. Check out [example_config.py](example_config.py) for configuration examples
3. Experiment with different settings to find what works best for your hardware!

---

**Happy coding! 🎉**
