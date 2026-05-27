# 🛡️Real-Time AI Anti-Distraction Assistant (FocusGuard)

FocusGuard is an intelligent, edge-computing productivity application designed to break the habit of digital distraction! 📱⚡ By continuously monitoring your webcam stream, the application tracks your facial positioning and physical smartphone proximity in real time. If a distraction is detected beyond a configurable grace period, the system triggers audible and visual alerts to snap you back to focus! 🧘‍♂️🔥

Built natively in Python using state-of-the-art computer vision models, FocusGuard operates **entirely locally**, ensuring maximum privacy and ultra-low latency. 🔒💻

---

## 🚀 Key Features

* **🔄 Dual-Model Synchronization:** Computes simultaneous tracking using **YOLOv8** for rapid object identification alongside **MediaPipe's Modern Tasks API** for robust face detection.
* **📏 Spatial Proximity Analysis:** Uses Euclidean distance formulas between the relative centers of your face and smartphone bounding boxes to differentiate between a phone merely sitting on a desk versus a phone actively in use.
* **⏳ Intelligent Grace Periods:** A configurable timer prevents false alarms during momentary tasks (e.g., viewing a 2FA authentication code).
* **🔒 100% Privacy Focused:** Your data never leaves your machine. Frame processing, mathematical tracking, and audio playback run locally in real time.

---

## 🛠️ Architecture & Tech Stack

* **🐍 Language:** Python 3.11+
* **👁️ Core Computer Vision:** OpenCV (Video capture & frame buffering)
* **🎯 Object Detection:** Ultralytics YOLOv8 (Nano variant for high-FPS CPU performance)
* **👤 Face Tracking Engine:** Google MediaPipe Tasks API (`blaze_face_short_range`)
* **🔊 Audio Pipeline:** Pygame Mixer API

### 📁 Project Structure

```text
anti-distraction-ai/
│
├── assets/                 # 📂 Audio clips and local ML model configurations
│   ├── scream.mp3          
│   └── blaze_face_short_range.tflite
│
├── config/                 # ⚙️ Dynamic system parameters
│   └── settings.json       
│
├── src/                    # 🛠️ Modularized source components
│   ├── __init__.py         
│   ├── detector.py         # 🧠 AI inference and coordinate extraction
│   └── audio_manager.py    # 🔊 Multi-threaded audio playback controls
│
├── main.py                 # 🎬 Core application controller & UI loop
├── requirements.txt        # 📦 Production dependencies
└── .gitignore              # 🚫 Environment isolation configurations

## 📦 Installation & Setup
Prerequisites
Python 3.11, 3.12, or 3.13

A connected webcam

1. Clone the Repository
Bash
git clone [https://github.com/Soladev83/anti-distraction-ai.git](https://github.com/Soladev83/anti-distraction-ai.git)
cd anti-distraction-ai

2. Set Up a Virtual Environment
Bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

3. Install Dependencies
Bash
pip install -r requirements.txt

4. Configure Your Assets
Download Google's official Face Detection asset: blaze_face_short_range.tflite and drop it into your assets/ directory.

Add your choice of notification or alert sound to the assets/ directory, naming the file scream.mp3.

⚙️ Configuration & Customization
You can adjust the system's sensitivity parameters inside config/settings.json without modifying any Python code:

JSON
{
    "yolo_confidence": 0.5,
    "grace_period_seconds": 2.0,
    "proximity_threshold_pixels": 350
}
yolo_confidence: Minimum confidence score (0.0 to 1.0) required to register your phone.

grace_period_seconds: The duration (in seconds) you can look at your phone before the alarm triggers.

proximity_threshold_pixels: The maximum pixel distance between your face and your phone to register an active distraction. Lower values require the phone to be closer to your face.

🏁 Execution
To run FocusGuard, make sure your virtual environment is active and execute:

Bash
python main.py
Press q inside the webcam frame preview window to safely terminate the application loop and release system hardware.

📝 License
Distributed under the MIT License. See LICENSE for more information.
