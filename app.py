from flask import Flask, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Variable global para guardar la última vez que el ESP32 hizo ping
last_ping = None

@app.route("/")
def home():
    global last_ping
    connected = False
    if last_ping and (datetime.utcnow() - last_ping) < timedelta(seconds=30):
        connected = True
    status = "Conectado ✅" if connected else "Desconectado ❌"
    return f"""
        <h1>Servidor de video ESP32-S3</h1>
        <p>Estado ESP32: <strong>{status}</strong></p>
    """

@app.route("/ping")
def ping():
    global last_ping
    last_ping = datetime.utcnow()
    return jsonify({"status": "ok"})
