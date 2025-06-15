from flask import Flask, Response
import cv2
import mss
import numpy as np

app = Flask(__name__)

def generate():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Main monitor
        while True:
            img = np.array(sct.grab(monitor))
            _, jpeg = cv2.imencode('.jpg', img)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
