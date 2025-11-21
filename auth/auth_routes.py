from flask import Blueprint, request, jsonify
from auth.auth_controller import login, register

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register_route():
    data = request.json
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing fields"}), 400

    if register(data["username"], data["password"]):
        return jsonify({"message": "User created"}), 201
    return jsonify({"error": "Username already exists"}), 400


@auth_bp.post("/login")
def login_route():
    data = request.json
    token = login(data["username"], data["password"])
    if not token:
        return jsonify({"error": "Invalid credentials"}), 400
    return jsonify({"token": token})
