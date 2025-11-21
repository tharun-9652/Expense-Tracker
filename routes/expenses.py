from flask import Blueprint, request, jsonify
from models.expense import get_all, add, update, delete
from utils.validators import validate_expense
from utils.auth_middleware import require_auth

expenses_bp = Blueprint("expenses", __name__)

@expenses_bp.get("/")
@require_auth
def list_expenses():
    month = request.args.get("month")
    return jsonify(get_all(month))

@expenses_bp.post("/")
@require_auth
def add_expense():
    data = request.get_json()
    error = validate_expense(data)
    if error:
        return jsonify({"error": error}), 400
    new_id = add(data)
    return jsonify({"id": new_id, **data}), 201

@expenses_bp.put("/<int:id>")
@require_auth
def update_expense(id):
    data = request.get_json()
    update(id, data)
    return jsonify({"status":"updated"})

@expenses_bp.delete("/<int:id>")
@require_auth
def delete_expense(id):
    delete(id)
    return jsonify({"status":"deleted"})
