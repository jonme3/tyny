from flask import Flask, jsonify, render_template, request
from datetime import datetime, timedelta
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static"
IMAGE_FILENAME = "latest.jpg"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

last_ping = None

@app.route("/")
def index():
    # Evita caching con timestamp para que siempre cargue la imagen actualizada
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
    # Aquí recibimos la imagen en RAW desde el body
    image_data = request.get_data()
    if not image_data:
        return jsonify({"error": "No se envió imagen"}), 400

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], IMAGE_FILENAME)
    with open(save_path, "wb") as f:
        f.write(image_data)

    print(f"📷 Imagen guardada en {save_path}")
    print(f"¿Archivo existe después de guardar? {os.path.isfile(save_path)}")
    return jsonify({"status": "imagen recibida"}), 200

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
