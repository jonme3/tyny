from flask import Flask, jsonify, render_template, request, send_from_directory
from datetime import datetime, timedelta
import os

app = Flask(__name__)
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

@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "No se envió imagen"}), 400
    image = request.files["image"]
    if image.filename == "":
        return jsonify({"error": "Nombre de archivo vacío"}), 400
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], IMAGE_FILENAME)
    image.save(save_path)
    print(f"📷 Imagen guardada en {save_path}")
    return jsonify({"status": "imagen recibida"}), 200
