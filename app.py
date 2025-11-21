from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.expenses import expenses_bp
from routes.reports import reports_bp
from routes.categories import categories_bp
from auth.auth_routes import auth_bp
from models.user import create_user_table
from flask_jwt_extended import JWTManager

import os

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

# Register API blueprints
app.register_blueprint(expenses_bp, url_prefix="/api/expenses")
app.register_blueprint(categories_bp, url_prefix="/api/categories")
app.register_blueprint(reports_bp, url_prefix="/api/reports")
app.register_blueprint(auth_bp, url_prefix="/api/auth")

# Serve frontend index
@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

# Serve static files from frontend/
@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory("frontend", path)

if __name__ == "__main__":
    print("Running on http://127.0.0.1:5000")
    app.run(debug=True)
