# 🚗🗑️ Smart Autonomous Waste Management Car

```
  ___  _   _  ___  _   _  ___  _      ___  _  _  ___
 / __|| \ | ||  _|| \ | |/ __|| |    / __|| || ||  _|
 \__ \|  \| || |_ |  \| |\__ \| |_  | (__ | __ || |_
 |___/|_|\__||___||_|\__||___/|___| \___||_||_||___|

 Autonomous · Smart · Real-time AI · Edge Deployment
```

> **A self-driving smart bin car powered by YOLOv8, OpenCV, and Arduino**
> Built as a graduation project — fully autonomous, real-world deployed.

**[Ahmed Adel Shosha](https://ahmed-a-shosha.github.io)** — AI Engineer & Team Leader

---

## 🎥 Demo Video

> 📹 [Watch the car in action → YouTube/Drive Link]

---

## 📸 Screenshots

| FORWARD — Lane Detection | STOP — Person Detected |
|--------------------------|------------------------|
| ![forward](images/forward.png) | ![stop](images/stop_person.png) |

| WAITING BIN 90% | Person Detection |
|-----------------|-----------------|
| ![waiting](images/waiting_bin.png) | ![detection](images/detection.png) |

---

## 🧠 How It Works

```
Bin fills up
    ↓
Arduino detects 90% fill via ultrasonic sensor
    ↓
Sends signal to Raspberry Pi
    ↓
Car starts moving autonomously
    ↓
YOLOv8 detects people → STOP if person ahead
    ↓
OpenCV lane detection → FORWARD / LEFT / RIGHT
    ↓
Car arrives at collection center → emptied → returns
```

---

## ⚙️ System Architecture

```
┌─────────────────────────────────────────────┐
│              Raspberry Pi 4                 │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ YOLOv8   │  │  OpenCV  │  │  Flask   │  │
│  │ Person   │  │  Lane    │  │  Stream  │  │
│  │Detection │  │Detection │  │  API     │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│                    │                        │
└────────────────────│────────────────────────┘
                     │ Serial (USB)
┌────────────────────│────────────────────────┐
│              Arduino UNO                    │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   Bin    │  │  Smart   │  │  Front   │  │
│  │Ultrasonic│  │   Lid    │  │ Obstacle │  │
│  │  Sensor  │  │  Servo   │  │  Sensor  │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │     4-Wheel DC Motor Drive (L298N)   │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## 🤖 AI Features

| Feature | Technology | Description |
|---------|-----------|-------------|
| Person Detection | YOLOv8 nano | Real-time detection, auto-stop on human presence |
| Lane Following | OpenCV (Canny + ROI) | Autonomous road navigation |
| Bin Level | Ultrasonic + Arduino | 70% alert, 90% auto-dispatch |
| Smart Lid | Servo + Ultrasonic | Opens automatically when someone approaches |
| Live Stream | Flask + MJPEG | Real-time camera feed via REST API |

---

## 🛠️ Tech Stack

**AI / Software**
```
Python · YOLOv8 (Ultralytics) · OpenCV · Flask
PySerial · NumPy · PiCamera2
```

**Hardware**
```
Raspberry Pi 4 · Arduino UNO · PiCamera2
Ultrasonic Sensors (x3) · Servo Motor
DC Motors (x4) · L298N Motor Driver
```

---

## 📁 Repository Structure

```
smart-waste-car/
│
├── 🐍 app.py              → AI engine (YOLOv8 + Lane Detection + Flask)
├── ⚙️  arduino.ino         → Arduino firmware (sensors + motors + servo)
├── 📸 images/             → Screenshots from live camera feed
│   ├── forward.png
│   ├── stop_person.png
│   ├── waiting_bin.png
│   └── detection.png
└── 📖 README.md
```

---

## 🚀 How to Run

### Requirements
```bash
pip install ultralytics opencv-python flask picamera2 pyserial numpy
```

### Run on Raspberry Pi
```bash
# Connect Arduino via USB
# Run the AI engine
python app.py

# Access live stream at:
# http://<raspberry-pi-ip>:5000
```

---

## 📊 Decision Logic

```python
if bin_level < 90%:
    → WAIT at station (people throw trash)

elif bin_level >= 90%:
    → START moving to collection center

    if person_detected:
        → STOP immediately (safety)
    else:
        if lane == CENTER:   → FORWARD
        if lane == LEFT:     → TURN LEFT
        if lane == RIGHT:    → TURN RIGHT
```

---

## 👥 Team

**Team Leader & AI Engineer:** Ahmed Adel Shosha
- Designed the full AI stack
- Implemented YOLOv8 integration
- Built lane detection algorithm
- Developed Flask API & live stream
- Integrated hardware-software communication

*Project also includes web dashboard and mobile app developed by team members.*

---

<div align="center">

**Ahmed Adel Shosha** — AI Engineer · Team Leader

[![Portfolio](https://img.shields.io/badge/🌐_Portfolio-black?style=flat-square)](https://ahmed-a-shosha.github.io)
[![LinkedIn](https://img.shields.io/badge/💼_LinkedIn-0077B5?style=flat-square)](https://linkedin.com/in/ahmed-a-shosha)
[![GitHub](https://img.shields.io/badge/🐙_GitHub-333?style=flat-square)](https://github.com/Ahmed-A-Shosha)

*⭐ Star this repo if you found it interesting!*

</div>
