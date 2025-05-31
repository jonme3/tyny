from flask import Flask, Response, render_template, request
import time
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static"
IMAGE_FILENAME = "latest.jpg"

def mjpeg_generator():
    boundary = "--frame"
    while True:
        image_path = os.path.join(UPLOAD_FOLDER, IMAGE_FILENAME)
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                frame = img_file.read()
            yield (b"%s\r\nContent-Type: image/jpeg\r\nContent-Length: %d\r\n\r\n" % (boundary.encode(), len(frame)))
            yield frame
            yield b"\r\n"
        time.sleep(0.03)  # ~30fps

@app.route("/upload", methods=["POST"])
def upload():
    if request.data:
        image_path = os.path.join(UPLOAD_FOLDER, IMAGE_FILENAME)
        with open(image_path, "wb") as f:
            f.write(request.data)
        print(f"📷 Imagen guardada en {image_path}")
        return "OK", 200
    else:
        return "No image data", 400

@app.route("/video_feed")
def video_feed():
    return Response(
        mjpeg_generator(),
        mimetype="multipart/x-mixed-replace; boundary=--frame",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
