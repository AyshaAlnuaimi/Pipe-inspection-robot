
from flask import Flask, Response
from picamera2 import Picamera2
import cv2

app = Flask(__name__)
picam2 = Picamera2()

picam2.configure(picam2.create_video_configuration(
    main={"size": (1280, 720)}))  # increased resolution

# --- manual focus control (focus nearer objects) ---
picam2.set_controls({"AfMode": 0})
picam2.set_controls({"LensPosition": 6.5})  # tweak this if needed

picam2.start()

def generate():
    while True:
        frame = picam2.capture_array()
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/video')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='0.0.0.0', port=8000)
