# UI Guide - Computer Vision System

This system comes with **3 different interfaces** to suit your needs:

## 🎨 Interface Options

### 1. 🖥️ Desktop GUI (Recommended for Real-time)
**Modern Tkinter-based desktop application**

- ✅ Professional dark theme interface
- ✅ Real-time video processing
- ✅ Live FPS monitoring
- ✅ Interactive feature toggles
- ✅ Pause/Resume functionality
- ✅ Screenshot capture

**Best for:** Real-time webcam processing, live demonstrations

**Launch:**
```bash
python gui_app.py
```

**Features:**
- Left control panel with all settings
- Large video display area
- Real-time statistics (FPS, people count, unique count)
- Easy-to-use controls
- Video file or webcam support

---

### 2. 🌐 Web Interface (Modern & Shareable)
**Gradio-based web application**

- ✅ Beautiful modern web UI
- ✅ No installation needed for viewers
- ✅ Works in any browser
- ✅ Shareable link option
- ✅ Image, video, and webcam support
- ✅ Tabbed interface

**Best for:** Demos, presentations, remote access, sharing with others

**Launch:**
```bash
python web_app.py
```

Then open your browser to: `http://localhost:7860`

**Features:**
- **Image Analysis Tab:** Upload and process single images
- **Video Analysis Tab:** Process entire videos
- **Live Webcam Tab:** Real-time webcam (frame-by-frame)
- **About Tab:** System information and documentation

**Share your work:**
```bash
# To create a public shareable link (optional)
# Edit web_app.py and set share=True in demo.launch()
```

---

### 3. ⌨️ Command Line (Lightweight)
**Terminal-based application**

- ✅ Minimal resource usage
- ✅ Scriptable and automatable
- ✅ Perfect for headless systems
- ✅ All features available via flags

**Best for:** Automation, servers, low-resource systems, scripts

**Launch:**
```bash
# Basic usage
python main.py

# With options
python main.py --auto-optimize --target-fps 15

# Process video file
python main.py --source video.mp4

# Disable specific features
python main.py --disable emotion_detection pose_detection
```

---

## 📊 Feature Comparison

| Feature | Desktop GUI | Web Interface | Command Line |
|---------|-------------|---------------|--------------|
| Real-time Video | ✅ Excellent | ⚠️ Limited | ✅ Excellent |
| Ease of Use | ✅✅ Very Easy | ✅✅✅ Easiest | ⚠️ Moderate |
| Remote Access | ❌ No | ✅ Yes | ✅ SSH |
| Resource Usage | Medium | Medium-High | Low |
| Share with Others | ❌ No | ✅ Yes | ❌ No |
| Screenshot/Save | ✅ Built-in | ✅ Built-in | ⌨️ Manual |
| Best Performance | ✅✅ | ⚠️ | ✅✅ |

---

## 🎯 Which Interface Should You Use?

### Use **Desktop GUI** if:
- You want real-time webcam processing
- You need the best performance
- You prefer visual controls
- You're doing live demonstrations

### Use **Web Interface** if:
- You want to share with others
- You prefer browser-based apps
- You're processing images or videos (not live)
- You want the prettiest interface
- You need remote access

### Use **Command Line** if:
- You're automating tasks
- You're on a server/headless system
- You want minimum resource usage
- You're comfortable with terminal commands

---

## 🖥️ Desktop GUI Quick Guide

### Interface Layout

```
┌─────────────────────────────────────────────────────────┐
│  ⚙️ Control Panel  │  📊 Statistics & Video Display    │
├───────────────────┼─────────────────────────────────────┤
│                   │  ┌─────────────────────────────┐  │
│ 📹 Video Source   │  │  ⚡ FPS  👥 People           │  │
│  ○ Webcam        │  │  💻 Device  🔍 Unique       │  │
│  ○ Video File    │  └─────────────────────────────┘  │
│  [Browse...]      │                                   │
│                   │  ┌─────────────────────────────┐  │
│ ✨ Features       │  │                             │  │
│  ☑ Face Detection│  │                             │  │
│  ☑ Person Count  │  │      Video Feed             │  │
│  ☑ Age Detection │  │                             │  │
│  ☑ Emotion       │  │                             │  │
│  ☑ Pose Detection│  │                             │  │
│  ...              │  └─────────────────────────────┘  │
│                   │                                   │
│ ⚡ Performance    │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  ☑ Auto-Optimize │  Status: Processing...            │
│  Target FPS: 15   │                                   │
│  [====    ]       │                                   │
│                   │                                   │
│ [▶️ Start ]       │                                   │
│ [⏸️ Pause ]       │                                   │
│ [⏹️ Stop  ]       │                                   │
│ [📸][🔄]          │                                   │
└───────────────────┴───────────────────────────────────┘
```

### Controls

**Source Selection:**
- Choose between Webcam (default camera) or Video File
- Click "Browse..." to select a video file

**Feature Toggles:**
- Click checkboxes to enable/disable features
- Changes apply when you start processing

**Performance Settings:**
- **Auto-Optimize:** Automatically disable features to maintain FPS
- **Target FPS:** Slide to set desired frame rate (5-30)
- **Device:** Shows GPU/CPU (auto-detected)

**Action Buttons:**
- **▶️ Start:** Begin processing
- **⏸️ Pause:** Pause/resume processing
- **⏹️ Stop:** Stop and release camera
- **📸 Screenshot:** Save current frame
- **🔄 Reset:** Reset person tracking database

**Keyboard Shortcuts:**
- Press buttons or use mouse

---

## 🌐 Web Interface Quick Guide

### Tabs

#### 📸 Image Analysis
1. Upload an image
2. Select features to enable
3. Adjust performance settings
4. Click "🚀 Process Image"
5. View results and statistics

#### 🎬 Video Analysis
1. Upload a video file
2. Click "🚀 Process Video"
3. Wait for processing (shows progress)
4. Download processed video

#### 📹 Live Webcam
1. Allow camera access
2. Webcam feed appears
3. Processing happens automatically
4. View results in real-time

#### ℹ️ About
- System information
- Feature descriptions
- Usage instructions

### Tips
- **Image tab** is fastest for single frames
- **Video tab** processes entire videos offline
- **Webcam tab** is for live demo (processes frame-by-frame)

---

## ⌨️ Command Line Quick Reference

### Basic Commands

```bash
# Start with webcam
python main.py

# Use video file
python main.py --source video.mp4

# Use specific camera (1, 2, etc.)
python main.py --source 1

# Enable auto-optimization
python main.py --auto-optimize --target-fps 15

# Force CPU mode
python main.py --device cpu

# Disable features
python main.py --disable age_detection emotion_detection pose_detection

# Combine options
python main.py --source 0 --auto-optimize --target-fps 20 --device auto
```

### Keyboard Shortcuts (during runtime)
- **Q** - Quit
- **S** - Save screenshot
- **R** - Reset tracking database

---

## 🎨 Desktop GUI Screenshots

### Main Interface
The desktop GUI features:
- **Dark theme** for reduced eye strain
- **Color-coded statistics** for easy reading
- **Real-time updates** without lag
- **Professional design** suitable for presentations

### Control Panel Features
- **Emoji icons** for visual clarity
- **Organized sections** (Source, Features, Performance, Actions)
- **Clear labels** for all options
- **Intuitive layout** - top to bottom workflow

---

## 🌐 Web Interface Screenshots

### Modern Design
The web interface features:
- **Gradio's modern theme** with soft colors
- **Tabbed organization** for different tasks
- **Responsive layout** works on any screen size
- **Professional appearance** for demos

### Interactive Elements
- **Drag-and-drop** image upload
- **Real-time preview** of processed results
- **Markdown statistics** with formatting
- **Progress bars** for video processing

---

## 🚀 Getting Started

### First Time Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Choose your interface:**
   - Desktop GUI: `python gui_app.py`
   - Web Interface: `python web_app.py`
   - Command Line: `python main.py`

3. **Start processing!**

### Recommended Workflow

**For Presentations:**
1. Use Desktop GUI for live demos
2. Enable all features you want to show
3. Use auto-optimize if needed
4. Take screenshots with 📸 button

**For Batch Processing:**
1. Use Command Line
2. Process multiple videos with scripts
3. Save results automatically

**For Sharing:**
1. Use Web Interface
2. Process images/videos
3. Share the link with others

---

## 🛠️ Customization

### Desktop GUI Themes
Edit `gui_app.py` to customize colors:
```python
# Line ~10: Change background color
self.root.configure(bg='#1e1e1e')  # Dark theme

# Line ~30+: Change panel colors
left_panel = tk.Frame(parent, bg='#252526')  # Panel color
```

### Web Interface
Edit `web_app.py` to customize:
```python
# Line ~330+: Change theme
gr.Blocks(theme=gr.themes.Soft())  # Try: Soft(), Glass(), Monochrome()

# Custom CSS available for advanced styling
```

---

## 💡 Tips & Tricks

### Desktop GUI
- **Resize window** for better view
- **Use Pause** instead of Stop to avoid reinitialization
- **Screenshots** are saved to current directory
- **Reset tracking** if you want to start counting unique people from zero

### Web Interface
- **Share mode:** Set `share=True` to get public link
- **Port change:** Edit `server_port=7860` for different port
- **Process locally:** Images/videos stay on your machine

### Command Line
- **Redirect output:** `python main.py > log.txt 2>&1`
- **Background mode:** `python main.py &` (Linux/Mac)
- **Auto-restart:** Use with systemd or supervisor

---

## 🆘 Troubleshooting

### Desktop GUI Issues

**Problem:** Window is blank/white
```bash
# Try updating Pillow
pip install --upgrade Pillow
```

**Problem:** Buttons don't work
- Make sure you're not running multiple instances
- Check terminal for error messages

### Web Interface Issues

**Problem:** Browser says "Connection refused"
- Make sure the app is running
- Check firewall settings
- Try http://127.0.0.1:7860 instead of localhost

**Problem:** Webcam doesn't work
- Allow camera permissions in browser
- Check browser console for errors

### General Issues

**Problem:** Low FPS in any interface
- Enable auto-optimize
- Disable heavy features (emotion, pose)
- Reduce input resolution in config.py

---

## 📚 Additional Resources

- **README.md** - Complete project documentation
- **QUICKSTART.md** - 5-minute setup guide
- **config.py** - All configuration options
- **example_config.py** - Pre-configured examples

---

**Enjoy your new beautiful interfaces! 🎉**
