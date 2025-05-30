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
    if last_ping and (datetime.utcnow() - last_ping) < timedelta(seconds=30):
        connected = True
    return jsonify({"connected": connected})


@app.route("/ping")
def ping():
    global last_ping
    last_ping = datetime.utcnow()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
