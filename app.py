from flask import Flask, jsonify, render_template, request, Response, stream_with_context
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import time

app = Flask(__name__)
CORS(app)  # Permite CORS para todas las rutas

UPLOAD_FOLDER = "static"
IMAGE_FILENAME = "latest.jpg"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

last_ping = None

@app.route("/")
def index():
    return render_template("index.html", image_url=f"/static/{IMAGE_FILENAME}?t={datetime.utcnow().timestamp()}")

@app.route("/status")
def status():
    global last_ping
    connected = False
    if last_ping and (datetime.utcnow() - last_ping) < timedelta(seconds=4):
        connected = True
    return jsonify({"connected": connected})

@app.route("/ping")
def ping():
    global last_ping
    last_ping = datetime.utcnow()
    print(f"🔁 Ping recibido: {last_ping}")
    return jsonify({"status": "ok"})

@app.route("/upload", methods=["POST"], strict_slashes=False)
def upload():
    if "image" not in request.files:
        return jsonify({"error": "No se envió imagen"}), 400
    
    image = request.files["image"]
    if image.filename == "":
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], IMAGE_FILENAME)
    image.save(save_path)
    print(f"📷 Imagen guardada en {save_path}")
    return jsonify({"status": "imagen recibida"}), 200

def generate_mjpeg():
    while True:
        img_path = os.path.join(app.config["UPLOAD_FOLDER"], IMAGE_FILENAME)
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                img = f.read()
            frame = (b"--frame\r\n"
                     b"Content-Type: image/jpeg\r\n\r\n" + img + b"\r\n")
            yield frame
        else:
            # Imagen no disponible, espera un poco
            time.sleep(0.1)
            continue
        time.sleep(0.033)  # Aproximadamente 30fps

@app.route("/video_feed")
def video_feed():
    return Response(stream_with_context(generate_mjpeg()),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/list_static")
def list_static():
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        return jsonify({"error": "Carpeta static no existe"})
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    print(f"Archivos en static/: {files}")
    return jsonify(files)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
