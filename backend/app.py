
from pathlib import Path

from flask import Flask, jsonify, send_from_directory
from recommendation_routes import recommendation_bp

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

app = Flask(__name__)

app.register_blueprint(recommendation_bp)


@app.get("/")
def home():
    return send_from_directory(str(FRONTEND_DIR), "index.html")


@app.get("/style.css")
def stylesheet():
    return send_from_directory(str(FRONTEND_DIR), "style.css")


@app.get("/app.js")
def javascript():
    return send_from_directory(str(FRONTEND_DIR), "app.js")


@app.get("/api/health")
def health_check():
    return jsonify({
        "status": "ok",
        "application": "StyleSense AI"
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
