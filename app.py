from flask import Flask, jsonify, render_template, request
from datetime import datetime, timedelta
import os

app = Flask(__name__)
last_ping = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    global last_ping
    connected = False
    if last_ping and (datetime.utcnow() - last_ping) < timedelta(seconds=30):
        connected = True
    return jsonify({"connected": connected})

@app.route("/ping")
def ping():
    global last_ping
    last_ping = datetime.utcnow()
    return jsonify({"status": "ok"})

@app.route("/upload", methods=["POST"])
def upload():
    if not request.data:
        return {"error": "No data received"}, 400

    # Guarda la imagen JPEG recibida en raw
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"uploads/frame_{timestamp}.jpg"
    os.makedirs("uploads", exist_ok=True)
    with open(filename, "wb") as f:
        f.write(request.data)

    print(f"Imagen guardada: {filename}")
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
