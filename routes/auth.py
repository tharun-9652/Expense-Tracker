from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from db.db import get_db

auth_bp = Blueprint("auth", __name__)

# ---------------- REGISTER ----------------
@auth_bp.post("/register")
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db()
    cur = conn.cursor()

    # Try creating new user
    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        conn.commit()
        return jsonify({"message": "User created successfully"}), 201

    except Exception as e:
        print("DB Error:", e)
        return jsonify({"error": "Username already exists"}), 409


# ---------------- LOGIN ----------------
@auth_bp.post("/login")
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    # Create JWT token
    token = create_access_token(identity=user["id"])

    return jsonify({"token": token})
