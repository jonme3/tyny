from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Servidor de video ESP32-S3'

@app.route('/upload', methods=['POST'])
def upload():
    image = request.data
    with open("latest.jpg", "wb") as f:
        f.write(image)
    return "OK", 200

@app.route('/frame')
def get_frame():
    if not os.path.exists("latest.jpg"):
        return "No image yet", 404
    return send_file("latest.jpg", mimetype='image/jpeg')
