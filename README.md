# 🎮 Gesture-Controlled Game Interface using Hand Tracking ✋

This project lets you **control any PC game (like Hill Climb Racing)** using **hand gestures** via webcam — without touching keyboard or mouse! It uses **MediaPipe**, **OpenCV**, and **PyAutoGUI** to detect your hand and simulate key/mouse actions.

---

## 🧠 Features

- ✅ Real-time hand tracking using webcam
- 🚘 Control games like Hill Climb Racing using:
  - Thumb gesture → Accelerate
  - Index gesture → Brake
  - Fist gesture → Reverse
- 🖱️ Menu Mode:
  - Move cursor with hand
  - Click using pinch gesture
- 🔁 Switch between **Game Mode** and **Menu Mode** using gestures
- 🪄 Smooth cursor movement with hand

---

## ✨ Gestures and Mappings

| Gesture                      | Action                 |
|-----------------------------|------------------------|
| ✋ All fingers open          | Cursor (Menu Mode)     |
| 👍 Thumb only up            | Accelerate             |
| ☝️ Index only up           | Brake                  |
| ✊ Fist (all fingers down)   | Reverse                |
| 🤏 Thumb + Index close      | Mouse Click / Tap      |

---

## 🔧 Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy
  
---

📷 Demo
(You can add a GIF or video link here later)

---

🙌 Acknowledgements

MediaPipe by Google

OpenCV

PyAutoGUI

---
💡 Future Improvements

Add gesture customization

Add gesture training module

Voice + gesture hybrid control

UI overlay with mode indicators
