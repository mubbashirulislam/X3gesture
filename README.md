# X3Gesture Tool 🖐

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A sophisticated computer automation tool that uses computer vision and machine learning to detect hand gestures in real-time and trigger customizable system actions. X3Gesture employs MediaPipe's hand tracking technology combined with custom gesture recognition algorithms to provide a hands-free control interface for your PC.

## Key Features

- **Real-time Hand Gesture Detection**: Utilizes MediaPipe's hand tracking for accurate gesture recognition
- **Customizable System Actions**: Trigger various system operations through hand gestures
- **User-friendly GUI**: Clean and intuitive interface for easy configuration
- **Robust Error Handling**: Comprehensive error management and logging system
- **Performance Optimization**: Configurable resolution settings and gesture cooldown
- **Consistent Gesture Recognition**: Multi-frame validation to prevent false positives

##  What Makes X3Gesture Unique

1. **Advanced Gesture Validation**
   - Implements a consecutive frame validation system
   - Requires multiple consistent detections before triggering actions
   - Reduces false positives while maintaining responsiveness

2. **Intelligent Finger Tracking**
   - Custom algorithms for precise finger position analysis
   - Special handling for thumb movement detection
   - Euclidean distance calculations for accurate gesture measurement

3. **Flexible Architecture**
   - Modular design separating GUI and core functionality
   - Callback-based action system for easy extensibility
   - Configurable parameters for customized operation

##  Technical Implementation

### Core Components

1. **X3GestureController (x3gesture_controller.py)**
   - Handles core gesture detection logic
   - Manages camera input and frame processing
   - Implements MediaPipe integration
   - Provides real-time visualization
   - Manages gesture state tracking

2. **X3GestureToolGUI (x3gesture_gui.py)**
   - Provides user interface for configuration
   - Handles system action execution
   - Manages user preferences
   - Implements notification system

### Gesture Detection Algorithm

The tool uses a sophisticated approach to detect hand gestures:

```python
# Pseudo-code representation of the gesture detection logic
1. Capture frame from camera
2. Process frame using MediaPipe Hands
3. Extract hand landmarks
4. Calculate finger positions and distances
5. Apply gesture recognition rules
6. Validate gesture across multiple frames
7. Trigger action if gesture is confirmed
```

## Requirements

Create a `requirements.txt` file with the following dependencies:

<antArtifact identifier="requirements-txt" type="application/vnd.ant.code" language="text" title="requirements.txt">
opencv-python>=4.7.0
mediapipe>=0.9.0
PyQt5>=5.15.0
numpy>=1.21.0


## Installation

1. Clone the repository:
```bash
git clone https://github.com/mubbashirulislam/x3gesture.git
cd x3gesture
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

##  Usage

1. Launch the application:
```bash
python x3gesture_gui.py
```

2. Configure settings in the GUI:
   - Set gesture cooldown time
   - Choose resolution mode
   - Select desired action for fist gesture
   - Click "Start Gesture Detection" to begin

3. Available actions:
   - Lock Screen
   - Open Calculator
   - Show Notification
   - Shutdown PC

## ⚙️ Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| Gesture Cooldown | Minimum time between gesture triggers | 1.0 seconds |
| Resolution Mode | High/Low resolution camera capture | Low |
| Camera Index | Device camera selection | 0 |
| Detection Confidence | Minimum confidence for hand detection | 0.7 |
| Tracking Confidence | Minimum confidence for hand tracking | 0.7 |

##  Performance Optimization

The tool includes several optimizations:

- **Frame Processing**
  - Configurable resolution for different performance needs
  - Efficient landmark calculation using NumPy operations
  - Memory-optimized frame handling

- **Gesture Recognition**
  - Multi-frame validation to reduce CPU usage
  - Cooldown mechanism to prevent action spam
  - Early exit conditions for non-matching gestures

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

