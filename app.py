from flask import Flask, Response, render_template, request
import time
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static"
IMAGE_FILENAME = "latest.jpg"

# MJPEG Stream Generator (envía continuamente imágenes JPEG)
def mjpeg_generator():
    image_path = os.path.join(UPLOAD_FOLDER, IMAGE_FILENAME)
    while True:
        if os.path.exists(image_path):
            try:
                with open(image_path, "rb") as img_file:
                    frame = img_file.read()
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )
            except Exception as e:
                print("Error leyendo imagen:", e)
        time.sleep(0.03)  # 30fps (33ms)

# Ruta para subir imagen desde ESP32
@app.route("/upload", methods=["POST"])
def upload():
    if request.data:
        image_path = os.path.join(UPLOAD_FOLDER, IMAGE_FILENAME)
        with open(image_path, "wb") as f:
            f.write(request.data)
        print(f"📷 Imagen recibida")
        return "OK", 200
    else:
        return "No image data", 400

# Ruta para ver MJPEG
@app.route("/video_feed")
def video_feed():
    return Response(
        mjpeg_generator(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

# Página principal
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
