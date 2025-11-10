# 🎥 Advanced Motion Detector Pro

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-active-success)

A professional-grade motion detection system with modern GUI, advanced analytics, and intelligent notifications.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Configuration](#-configuration) • [Screenshots](#-screenshots)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [Advanced Features](#-advanced-features)
- [Troubleshooting](#-troubleshooting)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**Advanced Motion Detector Pro** is a sophisticated motion detection application built with Python and OpenCV. It features a beautiful modern GUI, multiple detection algorithms, real-time video recording, comprehensive analytics, and intelligent notification systems.

Perfect for:
- 🏠 Home security monitoring
- 🔬 Scientific observation and research
- 🎮 Gaming and streaming applications
- 📊 Behavioral analytics
- 🛡️ Security and surveillance systems

---

## ✨ Features

### Core Detection Features
- 🎯 **Multiple Detection Algorithms**
  - Simple frame difference detection
  - Advanced MOG2 background subtraction
  - Configurable sensitivity and thresholds

- 🎥 **Smart Video Recording**
  - Automatic recording on motion detection
  - Manual snapshot capture
  - Multiple codec support (MP4, AVI)
  - Organized file management

- 🖥️ **Modern User Interface**
  - Dark theme with customtkinter
  - Real-time video preview
  - Live statistics and FPS counter
  - Intuitive controls and settings

### Analytics & Visualization
- 📊 **Comprehensive Statistics**
  - Total detections and duration tracking
  - Average event duration calculation
  - Hourly and daily activity patterns
  - Peak activity identification

- 📈 **Advanced Visualizations**
  - Hourly distribution bar charts
  - Daily activity patterns
  - Duration histograms
  - Activity heatmaps
  - Timeline visualization
  - HTML report generation

### Notifications
- 🔔 **Multi-channel Alerts**
  - Desktop notifications (cross-platform)
  - Email notifications (SMTP)
  - Discord webhook integration
  - Slack webhook integration
  - Configurable cooldown periods

### Data Management
- 💾 **Export Capabilities**
  - CSV export for event data
  - HTML comprehensive reports
  - Pandas DataFrame integration
  - JSON configuration files

---

## 💻 Requirements

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Webcam**: Any USB or built-in camera
- **Storage**: 1GB free space for recordings

### Python Dependencies
All dependencies are automatically installed via the setup script:
- opencv-python >= 4.8.0
- numpy >= 1.24.0
- pandas >= 2.0.0
- customtkinter >= 5.2.0
- pillow >= 10.0.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- plyer >= 2.1.0
- requests >= 2.31.0

---

## 🚀 Installation

### Linux / macOS

1. **Clone the repository** (or download the files)
   ```bash
   cd /path/to/Motions-Detector
   ```

2. **Make scripts executable**
   ```bash
   chmod +x setup.sh run.sh
   ```

3. **Run the setup script**
   ```bash
   ./setup.sh
   ```

   The setup script will:
   - ✅ Check Python installation and version
   - ✅ Create a virtual environment
   - ✅ Install all dependencies
   - ✅ Create necessary directories
   - ✅ Generate default configuration

### Windows

1. **Navigate to the project folder**
   ```cmd
   cd C:\path\to\Motions-Detector
   ```

2. **Run the setup script**
   ```cmd
   setup.bat
   ```

   The setup script will:
   - ✅ Check Python installation
   - ✅ Create a virtual environment
   - ✅ Install all dependencies
   - ✅ Create necessary directories
   - ✅ Generate default configuration

---

## 🎯 Quick Start

### Linux / macOS
```bash
./run.sh
```

### Windows
```cmd
run.bat
```

### First Run Steps

1. **Start Detection**
   - Click the "▶ Start Detection" button
   - Allow camera access if prompted

2. **Adjust Settings**
   - Go to the "Settings" tab
   - Adjust sensitivity and detection parameters
   - Enable auto-recording if desired

3. **Monitor Activity**
   - Watch the live video feed
   - Check the "Statistics" tab for analytics
   - View recent events in the "Events" tab

4. **Stop Detection**
   - Click "⏹ Stop Detection" when done
   - Review statistics and export data if needed

---

## 📖 Usage Guide

### Main Interface

#### Control Panel
- **▶ Start Detection**: Begin motion detection
- **⏹ Stop Detection**: Stop detection and save events
- **📷 Snapshot**: Capture current frame

#### Status Bar
- **Status**: Current system state (Idle/Running/Stopped)
- **Detections**: Total number of motion events
- **Recording Status**: Shows if video is being recorded

### Settings Tab

#### Detection Settings
- **Algorithm**: Choose between 'simple' or 'mog2'
  - `simple`: Fast, good for controlled environments
  - `mog2`: Advanced, better for complex scenes

- **Sensitivity** (10-100): Lower = less sensitive, Higher = more sensitive
  - Low (10-30): Only large movements
  - Medium (40-60): Balanced detection
  - High (70-100): Very sensitive, may detect shadows

- **Minimum Motion Area** (1000-20000): Minimum pixel area to trigger detection
  - Small (1000-5000): Detect small objects
  - Medium (5000-10000): General purpose
  - Large (10000+): Only large movements

#### Recording Settings
- **Auto-record on motion**: Automatically save video when motion is detected
- Videos are saved to the `recordings/` directory

### Statistics Tab

View real-time statistics:
- Total number of detections
- Total duration of all events
- Last detection timestamp
- Average event duration

Click "Refresh Statistics" to update the display.

### Events Tab

- View chronological list of recent motion events
- Shows start time and duration for each event
- Clear history with "Clear Event History" button

### Exporting Data

#### Export to CSV
1. Go to Settings tab
2. Click "Export Events to CSV"
3. Choose save location
4. Open in Excel or any spreadsheet application

#### Generate HTML Report
Run this in the Python console:
```python
from statistics_visualizer import StatisticsVisualizer
visualizer = StatisticsVisualizer(detector.get_motion_events())
visualizer.export_to_html_report("motion_report.html")
```

---

## ⚙️ Configuration

Configuration is stored in `config.json`. The file is created automatically with defaults.

### Configuration Structure

```json
{
    "camera": {
        "index": 0,           // Camera device index (0 = default)
        "width": 640,         // Frame width
        "height": 480,        // Frame height
        "fps": 30             // Frames per second
    },
    "detection": {
        "algorithm": "mog2",  // Detection algorithm: "simple" or "mog2"
        "sensitivity": 50,    // Threshold for motion (0-100)
        "min_area": 5000,     // Minimum area in pixels
        "bg_threshold": 16,   // Background subtractor threshold
        "blur_kernel": 21,    // Gaussian blur kernel size
        "dilation_iterations": 2  // Morphological dilation
    },
    "recording": {
        "enabled": true,      // Auto-record on motion
        "codec": "mp4v",      // Video codec (mp4v, XVID, etc.)
        "output_dir": "recordings"  // Output directory
    },
    "notifications": {
        "enabled": false,     // Enable notifications
        "cooldown": 60,       // Seconds between notifications
        "desktop_enabled": true,   // Desktop notifications
        "email_enabled": false     // Email notifications
    }
}
```

### Email Notifications Setup

Add to your `config.json`:

```json
{
    "notifications": {
        "enabled": true,
        "email_enabled": true,
        "email": {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender": "your-email@gmail.com",
            "password": "your-app-password",
            "recipient": "recipient@email.com"
        }
    }
}
```

**Note for Gmail users**: Use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password.

### Discord Notifications Setup

Add to your `config.json`:

```json
{
    "notifications": {
        "enabled": true,
        "discord_webhook": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
    }
}
```

---

## 🔥 Advanced Features

### Custom Detection Algorithms

You can extend `motion_detector_core.py` to add your own algorithms:

```python
def detect_motion_custom(self, frame: np.ndarray) -> Tuple[bool, np.ndarray, List]:
    """
    Your custom detection algorithm
    """
    # Implement your algorithm here
    motion = False
    processed_frame = frame.copy()
    contours = []

    # ... your detection logic ...

    return motion, processed_frame, contours
```

### Multi-Camera Support

To use multiple cameras, modify the configuration:

```json
{
    "camera": {
        "index": 1  // Change to 1, 2, 3... for different cameras
    }
}
```

### Performance Optimization

For better performance:
1. Reduce camera resolution:
   ```json
   "camera": {
       "width": 320,
       "height": 240
   }
   ```

2. Increase minimum area:
   ```json
   "detection": {
       "min_area": 10000
   }
   ```

3. Use simple algorithm for faster processing

### Recording Customization

Change video codec:
```json
{
    "recording": {
        "codec": "XVID"  // or "MJPG", "H264", etc.
    }
}
```

---

## 🐛 Troubleshooting

### Camera Not Working

**Problem**: "Failed to initialize camera"

**Solutions**:
1. Check if camera is connected and working
2. Try different camera index (0, 1, 2...)
3. Close other applications using the camera
4. Check camera permissions (especially on macOS/Linux)

Linux camera permissions:
```bash
sudo usermod -a -G video $USER
# Log out and back in
```

### GUI Not Loading

**Problem**: "No module named 'customtkinter'"

**Solution**: Re-run setup script
```bash
./setup.sh  # Linux/macOS
setup.bat   # Windows
```

### Poor Detection Performance

**Problem**: Too many false positives or missed detections

**Solutions**:
1. Adjust sensitivity in Settings tab
2. Increase minimum area threshold
3. Switch to MOG2 algorithm
4. Improve lighting conditions
5. Reduce background movement (fans, curtains, etc.)

### High CPU Usage

**Solutions**:
1. Reduce camera resolution
2. Lower FPS setting
3. Use simple algorithm instead of MOG2
4. Increase minimum area threshold

### Recording Issues

**Problem**: Videos won't play or are corrupted

**Solutions**:
1. Try different codec (mp4v, XVID, MJPG)
2. Check available disk space
3. Ensure write permissions for recordings folder
4. Install video codecs on your system

---

## 📁 Project Structure

```
Motions-Detector/
├── motion_detector_core.py      # Core detection engine
├── motion_detector_gui.py       # GUI application
├── notification_system.py       # Notification handlers
├── statistics_visualizer.py     # Analytics and visualization
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup file
├── config.json                  # Configuration file
├── setup.sh                     # Linux/macOS setup script
├── setup.bat                    # Windows setup script
├── run.sh                       # Linux/macOS run script
├── run.bat                      # Windows run script
├── README.md                    # This file
├── S1.py                        # Legacy/original script
├── data.csv                     # Historical event data
├── venv/                        # Virtual environment (created by setup)
├── recordings/                  # Video recordings (created by setup)
├── snapshots/                   # Camera snapshots (created by setup)
└── exports/                     # Exported data (created by setup)
```

---

## 🔧 Development

### Running Tests

```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pytest tests/
```

### Code Formatting

```bash
black *.py
flake8 *.py
```

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🐛 Report bugs and issues
2. 💡 Suggest new features
3. 📝 Improve documentation
4. 🔧 Submit pull requests

Please read the contributing guidelines before submitting.

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

- **Developer**: Mahmoud Tolba (Solo Developer)
- **GitHub**: [@mahmoudtolba-tech](https://github.com/mahmoudtolba-tech)
- **Version**: 2.0.0
- **Year**: 2024

## 🙏 Acknowledgments

- OpenCV community for excellent computer vision library
- CustomTkinter for modern GUI components
- All contributors and users

---

## 📞 Support

For support, questions, or feature requests:

- 📧 Email: support@motiondetector.example
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/motion-detector/issues)
- 📖 Documentation: This README and inline code comments

---

## 🎉 Version History

### v2.0.0 (2024)
- ✨ Complete rewrite with modern architecture
- 🎨 Beautiful dark-themed GUI
- 📊 Advanced analytics and visualizations
- 🔔 Multi-channel notification system
- 💾 Enhanced data export capabilities
- 🎥 Improved video recording
- ⚙️ Comprehensive configuration system

### v1.0.0 (2020)
- 🎯 Basic motion detection
- 📹 Simple video capture
- 📝 CSV data logging

---

<div align="center">

**Made with ❤️ and Python**

⭐ Star this project if you find it useful!

</div>
