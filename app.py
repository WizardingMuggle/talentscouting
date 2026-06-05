from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder=".")
CORS(app)

DATA_FILE = "candidates.json"


def load_candidates():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_candidates(candidates):
    with open(DATA_FILE, "w") as f:
        json.dump(candidates, f, indent=2)


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/apply")
def apply():
    return send_from_directory(".", "apply.html")


@app.route("/careers")
def careers():
    return send_from_directory(".", "careers.html")


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()

    required = ["name", "email", "linkedin", "skills", "role"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    candidate = {
        "id": datetime.utcnow().strftime("%Y%m%d%H%M%S%f"),
        "submitted_at": datetime.utcnow().isoformat() + "Z",
        "name": data["name"].strip(),
        "email": data["email"].strip(),
        "linkedin": data["linkedin"].strip(),
        "github": data.get("github", "").strip(),
        "role": data["role"].strip(),
        "experience": data.get("experience", "").strip(),
        "skills": [s.strip() for s in data["skills"] if s.strip()],
        "is_fresher": bool(data.get("is_fresher", False)),
        "current_org": None if data.get("is_fresher") else data.get("current_org", ""),
        "notice_period": None if data.get("is_fresher") else data.get("notice_period"),
        "bio": data.get("bio", "").strip(),
    }

    candidates = load_candidates()
    candidates.append(candidate)
    save_candidates(candidates)

    return jsonify({"message": "Application submitted successfully!", "id": candidate["id"]}), 201


@app.route("/candidates", methods=["GET"])
def get_candidates():
    return jsonify(load_candidates())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
