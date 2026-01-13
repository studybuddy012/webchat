from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime
from database import get_db

SECRET = "webchat-secret"

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchone()

    if user:
        if not check_password_hash(user["password"], password):
            return jsonify({"error":"Wrong password"}),401
        uid = user["id"]
    else:
        db.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (username, generate_password_hash(password))
        )
        db.commit()
        uid = db.execute(
            "SELECT id FROM users WHERE username=?",
            (username,)
        ).fetchone()["id"]

    token = jwt.encode({
        "user_id":uid,
        "username":username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, SECRET, algorithm="HS256")

    return jsonify({"token":token,"username":username})
from werkzeug.security import check_password_hash, generate_password_hash

@auth.route("/change-password", methods=["POST"])
def change_password():
    data = request.json
    username = data.get("username")
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user["password"], old_password):
        return jsonify({"error": "Old password wrong"}), 401

    new_hash = generate_password_hash(new_password)

    db.execute(
        "UPDATE users SET password=? WHERE username=?",
        (new_hash, username)
    )
    db.commit()

    return jsonify({"success": True})
