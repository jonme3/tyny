from flask import Flask, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
last_ping = None

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
