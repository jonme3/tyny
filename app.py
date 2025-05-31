from flask import Flask, Response, render_template, request
import time
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static"
IMAGE_FILENAME = "latest.jpg"
last_mtime = 0  # Marca de tiempo de la última imagen

def mjpeg_generator():
    global last_mtime
    while True:
        image_path = os.path.join(UPLOAD_FOLDER, IMAGE_FILENAME)
        if os.path.exists(image_path):
            mtime = os.path.getmtime(image_path)
            if mtime != last_mtime:
                last_mtime = mtime
                with open(image_path, "rb") as img_file:
                    frame = img_file.read()
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        time.sleep(0.01)  # Revisa frecuentemente para baja latencia

@app.route("/upload", methods=["POST"])
def upload():
    if request.data:
        image_path = os.path.join(UPLOAD_FOLDER, IMAGE_FILENAME)
        with open(image_path, "wb") as f:
            f.write(request.data)
        return "OK", 200
    return "No image data", 400

@app.route("/video_feed")
def video_feed():
    return Response(
        mjpeg_generator(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
