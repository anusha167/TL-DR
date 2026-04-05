from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

CORS(app, resources={r"/*": {"origins": "*"}})

DB_PATH = os.path.join(os.path.dirname(__file__), "tldr.db")
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed BOOLEAN DEFAULT FALSE
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            title TEXT,
            summary TEXT,
            audio_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/save-url", methods=["POST"])
def save_url():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "no url provided"}), 400

    conn = get_db()
    conn.execute("INSERT INTO urls (url) VALUES (?)", (url,))
    conn.commit()
    conn.close()

    # Process immediately in background
    from threading import Thread
    from agent import process_single_url
    from summarizer import summarize
    from tts import generate_audio
    from emailer import send_notification

    def process():
        content, title = process_single_url(url)
        if content:
            summary = summarize(content)
            audio_path = generate_audio(summary, url)

            conn2 = get_db()
            conn2.execute(
                "INSERT INTO summaries (url, title, summary, audio_path) VALUES (?, ?, ?, ?)",
                (url, title, summary, audio_path)
            )
            conn2.execute(
                "UPDATE urls SET processed = TRUE WHERE url = ?", (url,)
            )
            conn2.commit()
            conn2.close()

            # Send email to all registered users
            users = get_db().execute("SELECT email FROM users").fetchall()
            for user in users:
                send_notification(user["email"], title, url)

    Thread(target=process).start()
    return jsonify({"message": "URL saved! Processing started..."}), 200

@app.route("/digest", methods=["GET"])
def get_digest():
    conn = get_db()
    summaries = conn.execute(
        "SELECT * FROM summaries ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return jsonify([dict(s) for s in summaries]), 200

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    if not email:
        return jsonify({"error": "no email provided"}), 400
    conn = get_db()
    conn.execute("INSERT OR IGNORE INTO users (email) VALUES (?)", (email,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Registered!"}), 200

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

@app.route("/")
def dashboard():
    return send_from_directory("../dashboard", "index.html")

@app.route("/<path:filename>")
def dashboard_files(filename):
    return send_from_directory("../dashboard", filename)

if __name__ == "__main__":
    init_db()
    print("TL;DR backend running on http://localhost:8080")
    app.run(debug=True, port=8080, host='127.0.0.1')