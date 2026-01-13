from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from database import init_db, get_db
from auth import auth
import os
import chat_socket

BASE = os.path.dirname(os.path.abspath(__file__))
CLIENT = os.path.join(BASE, "..", "client")

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

chat_socket.register_events(socketio)
app.register_blueprint(auth)

@app.route("/")
def login_page():
    return send_from_directory(CLIENT, "login.html")

@app.route("/chat")
def chat_page():
    return send_from_directory(CLIENT, "chat.html")

@app.route("/messages/<room>")
def get_messages(room):
    db = get_db()
    rows = db.execute(
        "SELECT sender,message FROM messages WHERE room=? ORDER BY id",
        (room,)
    ).fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    init_db()
    socketio.run(app, host="0.0.0.0", port=10000)

