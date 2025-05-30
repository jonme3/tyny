from flask import Flask, jsonify, Response
from datetime import datetime, timedelta

app = Flask(__name__)
last_ping = None

# Ruta que sirve la página HTML con el video y el estado
@app.route("/")
def index():
    html = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Video ESP32-S3</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #121212;
      color: #eee;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 1em;
    }
    h1 {
      margin-bottom: 0.5em;
    }
    #status {
      font-size: 1.5em;
      font-weight: bold;
      padding: 0.4em 0.8em;
      border-radius: 8px;
      margin-bottom: 1em;
      user-select: none;
      border: 2px solid #f44336;
      color: #f44336;
      box-shadow: 0 0 8px #f4433699;
      transition: all 0.3s ease;
    }
    #status.connected {
      border-color: #4CAF50;
      color: #4CAF50;
      box-shadow: 0 0 8px #4CAF5099;
    }
    img {
      max-width: 100%;
      border-radius: 8px;
      box-shadow: 0 0 12px #000;
    }
  </style>
</head>
<body>
  <h1>Video en vivo</h1>
  <div id="status">Estado ESP32: Desconectado ❌</div>
  <img id="stream" src="" width="640" alt="Stream de video" />

  <script>
    const streamUrl = "/frame";  // Usa ruta relativa para evitar problemas CORS
    const statusDiv = document.getElementById("status");
    const img = document.getElementById("stream");

    // Actualiza el video cada 100ms (10 FPS)
    setInterval(() => {
      img.src = streamUrl + "?t=" + Date.now();
    }, 100);

    // Función para consultar estado de conexión ESP32
    async function checkStatus() {
      try {
        const resp = await fetch("/status");
        if (!resp.ok) throw new Error("Error en la respuesta");
        const data = await resp.json();

        if (data.connected) {
          statusDiv.textContent = "Estado ESP32: Conectado ✅";
          statusDiv.classList.add("connected");
        } else {
          statusDiv.textContent = "Estado ESP32: Desconectado ❌";
          statusDiv.classList.remove("connected");
        }
      } catch (e) {
        statusDiv.textContent = "Estado ESP32: Error al consultar";
        statusDiv.classList.remove("connected");
      }
    }

    // Consultar estado cada 10 segundos
    checkStatus();
    setInterval(checkStatus, 10000);
  </script>
</body>
</html>
