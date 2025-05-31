@app.route("/upload", methods=["POST"], strict_slashes=False)
def upload():
    # El ESP32 envía la imagen como raw bytes, no como "image" en form-data
    image_data = request.get_data()
    if not image_data:
        return jsonify({"error": "No se envió imagen"}), 400

    # Asegura que carpeta existe
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], IMAGE_FILENAME)
    with open(save_path, "wb") as f:
        f.write(image_data)

    print(f"📷 Imagen guardada en {save_path}")
    print(f"¿Archivo existe después de guardar? {os.path.isfile(save_path)}")
    return jsonify({"status": "imagen recibida"}), 200
