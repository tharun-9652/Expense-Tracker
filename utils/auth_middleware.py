from flask import request, jsonify
from utils.jwt_utils import decode_token

def require_auth(fn):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401
        
        token = token.split(" ")[1]
        payload = decode_token(token)

        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        request.user_id = payload["user_id"]
        return fn(*args, **kwargs)
    
    wrapper.__name__ = fn.__name__
    return wrapper
