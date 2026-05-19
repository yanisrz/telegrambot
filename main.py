import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not username and not email:
        return jsonify({"error": "At least one of username or email is required"}), 400
    if not password:
        return jsonify({"error": "password is required"}), 400
    lines = ["New registration:"]
    if username:
        lines.append(f"Username: {username}")
    if email:
        lines.append(f"Email: {email}")
    message = "\n".join(lines)
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(telegram_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message})
    return jsonify({"success": True, "message": "Registered and notified"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
