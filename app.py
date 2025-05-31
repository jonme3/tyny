from flask import Flask, Response, render_template
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
        time.sleep(0.1)  # 10 fps

@app.route("/video_feed")
def video_feed():
    return Response(
        mjpeg_generator(),
        mimetype="multipart/x-mixed-replace; boundary=--frame"
    )

@app.route("/")
def index():
    # Página con un <img> apuntando a /video_feed
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
