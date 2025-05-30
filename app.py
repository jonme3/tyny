from flask import Flask, jsonify, render_template
from datetime import datetime, timedelta

app = Flask(__name__)
last_ping = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    global last_ping
    connected = False
    # Verifica si el último ping fue hace menos de 30 segundos
    if last_ping and (datetime.utcnow() - last_ping) < timedelta(seconds=4):
        connected = True
    return jsonify({"connected": connected})

@app.route("/ping")
def ping():
    global last_ping
    last_ping = datetime.utcnow()
    print(f"🔁 Ping recibido: {last_ping}")
    return jsonify({"status": "ok"})
