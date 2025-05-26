# main.py
import os
import io
import base64
import numpy as np
import cv2
import onnxruntime as ort
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Cargar el modelo ONNX
model_path = "models/tinypose.onnx"  # Cambia esto si usas otro nombre o ruta
session = ort.InferenceSession(model_path)

# Preprocesamiento
def preprocess(image):
    img_resized = cv2.resize(image, (192, 256))  # resolución de entrada típica
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    img_input = img_rgb.astype(np.float32) / 255.0
    img_input = img_input.transpose(2, 0, 1)[np.newaxis, ...]  # NCHW
    return img_input

# Postprocesamiento (depende del modelo exacto que uses)
def postprocess(output):
    keypoints = output[0].reshape(-1, 3)  # x, y, score
    return keypoints.tolist()

@app.route("/detect", methods=["POST"])
def detect_pose():
    if "image" in request.files:
        file = request.files["image"]
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    else:
        data = request.get_json()
        if not data or "image_base64" not in data:
            return jsonify({"error": "No image provided"}), 400
        img_data = base64.b64decode(data["image_base64"])
        image = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)

    input_tensor = preprocess(image)
    outputs = session.run(None, {"input": input_tensor})
    keypoints = postprocess(outputs)
    return jsonify({"keypoints": keypoints})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
