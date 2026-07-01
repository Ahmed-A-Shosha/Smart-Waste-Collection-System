from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import numpy as np
from ultralytics import YOLO
import serial
import time

app = Flask(__name__)

# =========================
# Arduino
# =========================
arduino = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)

allow_movement = False
last_sent_cmd = None

def send(cmd):
    global last_sent_cmd
    if cmd != last_sent_cmd:
        try:
            arduino.write(cmd.encode())
            last_sent_cmd = cmd
        except:
            pass

def read_from_arduino():
    global allow_movement
    try:
        while arduino.in_waiting:
            msg = arduino.readline().decode(errors='ignore').strip()
            if not msg:
                continue

            print(msg)

            if msg == "BIN_70":
                print("🚨 Bin reached 70%")

            elif msg == "BIN_MOVING":
                print("🚗 Bin reached 90% and movement enabled")
                allow_movement = True

            elif msg.startswith("LEVEL:"):
                pass

    except:
        pass

# =========================
# YOLO
# =========================
model = YOLO("yolov8n.pt")

# =========================
# Camera
# =========================
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

# =========================
# Lane Detection
# =========================
def get_direction(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    h, w = edges.shape
    roi = edges[h//2:, :]
    idx = np.where(roi > 0)

    if len(idx[1]) == 0:
        return "STOP"

    avg = np.mean(idx[1])
    center = w / 2

    if avg < center - 40:
        return "LEFT"
    elif avg > center + 40:
        return "RIGHT"
    else:
        return "FORWARD"

# =========================
def generate_frames():
    global allow_movement

    while True:
        read_from_arduino()

        frame = picam2.capture_array()

        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # YOLO
        results = model(frame, imgsz=320, verbose=False)

        detected_person = False

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                if label == "person":
                    detected_person = True

        # =========================
        # Decision
        # =========================
        if not allow_movement:
            send('S')
            status = "WAITING BIN 90%"
        else:
            if detected_person:
                send('S')
                status = "STOP (PERSON)"
            else:
                direction = get_direction(frame)

                if direction == "FORWARD":
                    send('F')
                elif direction == "LEFT":
                    send('L')
                elif direction == "RIGHT":
                    send('R')
                else:
                    send('S')

                status = direction

        cv2.putText(
            frame,
            status,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )

@app.route('/')
def video():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

app.run(host='0.0.0.0', port=5000)
