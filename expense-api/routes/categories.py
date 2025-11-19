from flask import Blueprint, request, jsonify
from models.category import get_all, add

categories_bp = Blueprint("categories", __name__)

@categories_bp.get("/")
def list_categories():
    return jsonify(get_all())

@categories_bp.post("/")
def add_category():
    data = request.get_json()
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "Category required"}), 400

    cid = add(name)
    return jsonify({"id": cid, "name": name}), 201
